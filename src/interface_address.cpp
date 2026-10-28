#include "src/interface_address.h"
#include <arpa/inet.h>
#include <algorithm>
#include <atomic>
#include <chrono>
#include <condition_variable>
#include <cstring>
#include <iomanip>
#include <sstream>
#include <thread>

namespace interface_address {
namespace {
constexpr size_t max_packet = 2048, queue_capacity = 64, max_addresses = 256;
constexpr unsigned packets_per_second = 100;
using Clock = std::chrono::steady_clock;
[[noreturn]] void fail(sai_status_t s, const std::string& m) { throw Error(s, m); }
void check(sai_status_t s, const std::string& m) { if (s != SAI_STATUS_SUCCESS) fail(s, m); }
void require(bool b, const std::string& m) { if (!b) fail(SAI_STATUS_INVALID_PARAMETER, m); }
bool equal(const uint8_t* a, const uint8_t* b, size_t n) { return std::memcmp(a, b, n) == 0; }
bool zero(const uint8_t* a, size_t n) { for (size_t i = 0; i < n; ++i) if (a[i]) return false; return true; }
bool unicast_mac(const uint8_t* a) { return !(a[0] & 1) && !zero(a, 6); }
bool ipv6_unicast(const uint8_t* p) {
    return !zero(p, 16) && p[0] != 255 && !(zero(p, 15) && p[15] == 1) &&
           !(zero(p, 10) && p[10] == 255 && p[11] == 255);
}
uint16_t be16(const uint8_t* p) { return uint16_t((unsigned(p[0]) << 8) | p[1]); }
void put16(uint8_t* p, uint16_t n) { p[0] = uint8_t(n >> 8); p[1] = uint8_t(n); }
uint32_t sum(const uint8_t* p, size_t n, uint32_t s = 0) {
    while (n >= 2) { s += be16(p); p += 2; n -= 2; }
    if (n) s += unsigned(*p) << 8;
    return s;
}
uint16_t icmp_checksum(const uint8_t* ip, size_t n) {
    uint32_t s = sum(ip + 8, 32) + uint32_t(n) + 58;
    s = sum(ip + 40, n, s);
    while (s >> 16) s = (s & 65535) + (s >> 16);
    return uint16_t(~s);
}
std::string hex(uint64_t n) { std::ostringstream s; s << "0x" << std::hex << n; return s.str(); }
uint64_t number(const std::string& s, uint64_t max, bool oid = false) {
    size_t i = 0; unsigned base = 10;
    if (oid && s.size() > 2 && s.substr(0, 2) == "0x") { i = 2; base = 16; }
    require(!s.empty() && s.size() <= 32 && i < s.size(), "invalid integer");
    uint64_t n = 0;
    for (; i < s.size(); ++i) {
        char c = s[i]; unsigned d = c >= '0' && c <= '9' ? c - '0' :
            c >= 'a' && c <= 'f' ? c - 'a' + 10 : c >= 'A' && c <= 'F' ? c - 'A' + 10 : 99;
        require(d < base && d <= max && n <= (max - d) / base, "invalid/out-of-range integer");
        n = n * base + d;
    }
    return n;
}
sai_object_id_t oid(const std::string& s) { auto n = number(s, UINT64_MAX, true); require(n != 0, "null OID"); return n; }
struct Address {
    Target target;
    sai_object_id_t rif = 0, port = 0;
    std::string cidr, key;
};
Address parse(sai_object_id_t rif, const std::string& cidr) {
    require(cidr.size() < 64 && cidr.find('\0') == std::string::npos, "invalid host CIDR");
    size_t slash = cidr.find('/'); require(slash != std::string::npos, "host address requires prefix length");
    Address a; a.rif = rif;
    auto ip = cidr.substr(0, slash);
    if (inet_pton(AF_INET, ip.c_str(), a.target.ip.data()) != 1) {
        require(inet_pton(AF_INET6, ip.c_str(), a.target.ip.data()) == 1, "invalid host IP");
        a.target.ipv6 = true;
    }
    const auto* p = a.target.ip.data();
    if (a.target.ipv6) require(ipv6_unicast(p), "IPv6 address must be native unicast, not unspecified/loopback/mapped");
    else require(p[0] != 0 && p[0] != 127 && p[0] < 224, "IPv4 address must be unicast, not unspecified/loopback");
    auto bits = number(cidr.substr(slash + 1), a.target.ipv6 ? 128 : 32);
    char b[INET6_ADDRSTRLEN]{};
    require(inet_ntop(a.target.ipv6 ? AF_INET6 : AF_INET, p, b, sizeof(b)) != nullptr, "cannot format IP");
    a.cidr = std::string(b) + "/" + std::to_string(bits); // Deliberately NOT masked.
    a.key = hex(rif) + "@" + a.cidr;
    return a;
}
Address key(const std::string& text) {
    auto at = text.find('@'); require(at != std::string::npos, "expected RIF@hostCIDR");
    return parse(oid(text.substr(0, at)), text.substr(at + 1));
}
std::string mactext(const std::array<uint8_t, 6>& m) {
    std::ostringstream s; s << std::hex << std::setfill('0');
    for (size_t i = 0; i < m.size(); ++i) { if (i) s << ':'; s << std::setw(2) << unsigned(m[i]); }
    return s.str();
}
struct Attachment {
    int32_t type = 0;
    sai_object_id_t vlan = 0, member = 0, bridge_port = 0, bridge = 0;
    uint16_t vid = 0;
    std::array<uint8_t, 6> mac{};
    bool operator==(const Attachment& o) const {
        return type == o.type && vlan == o.vlan && member == o.member && bridge_port == o.bridge_port &&
               bridge == o.bridge && vid == o.vid && mac == o.mac;
    }
};
struct Record { Address address; Attachment attachment; };
struct Packet {
    std::array<uint8_t, max_packet> data{};
    size_t size = 0;
    sai_object_id_t port = 0, trap = 0;
    uint64_t generation = 0;
};
struct Service {
    std::mutex lifecycle, control, queue_mutex;
    std::condition_variable wake;
    std::thread worker;
    bool running = false, accepting = false, quitting = true, faulted = false;
    sai_object_id_t sw = 0;
    Sdk sdk;
    Options options;
    std::mutex* sai_mutex = nullptr;
    sai_hostif_api_t* hostif = nullptr;
    sai_switch_api_t* switch_api = nullptr;
    sai_router_interface_api_t* rif_api = nullptr;
    sai_vlan_api_t* vlan_api = nullptr;
    sai_bridge_api_t* bridge_api = nullptr;
    sai_port_api_t* port_api = nullptr;
    std::map<std::string, Record> records;
    Status stats;
    std::array<Packet, queue_capacity> queue;
    size_t head = 0, used = 0;
    unsigned window_packets = 0;
    Clock::time_point window = Clock::now();
    std::atomic<uint64_t> generation{0}, dropped{0}, admitted{0};
    // Main must stop before SDK teardown. This fallback only joins, never calls SDK.
    ~Service() {
        { std::lock_guard<std::mutex> l(queue_mutex); accepting = false; quitting = true; }
        wake.notify_all();
        if (worker.joinable()) worker.join();
    }
    template<class T> T* api(sai_api_t id) {
        T* p = nullptr; check(sdk.query(id, reinterpret_cast<void**>(&p)), "SAI API query " + std::to_string(id));
        if (!p) fail(SAI_STATUS_NOT_SUPPORTED, "null SAI API table");
        return p;
    }
    void identity(sai_object_id_t id, sai_object_type_t type) {
        require(id && sdk.object_type(id) == type && sdk.switch_id(id) == sw, "object type/switch mismatch: " + hex(id));
    }
    template<class F> sai_attribute_value_t read(F fn, sai_object_id_t id, sai_attr_id_t attr) {
        sai_attribute_t a{}; a.id = attr;
        check(fn(id, 1, &a), "SAI get " + hex(id) + " attr " + std::to_string(attr)); return a.value;
    }
    Attachment validate(const Address& a) {
        identity(a.rif, SAI_OBJECT_TYPE_ROUTER_INTERFACE); identity(a.port, SAI_OBJECT_TYPE_PORT);
        require(read(port_api->get_port_attribute, a.port, SAI_PORT_ATTR_TYPE).s32 == SAI_PORT_TYPE_LOGICAL, "not a physical logical port");
        Attachment t;
        t.type = read(rif_api->get_router_interface_attribute, a.rif, SAI_ROUTER_INTERFACE_ATTR_TYPE).s32;
        auto m = read(rif_api->get_router_interface_attribute, a.rif, SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS);
        std::copy(m.mac, m.mac + 6, t.mac.begin()); require(unicast_mac(t.mac.data()), "RIF MAC is not valid unicast");
        require(read(rif_api->get_router_interface_attribute, a.rif, a.target.ipv6 ?
            SAI_ROUTER_INTERFACE_ATTR_ADMIN_V6_STATE : SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE).booldata, "RIF protocol disabled");
        if (t.type == SAI_ROUTER_INTERFACE_TYPE_PORT) {
            require(read(rif_api->get_router_interface_attribute, a.rif, SAI_ROUTER_INTERFACE_ATTR_PORT_ID).oid == a.port, "routed RIF attachment mismatch");
        } else if (t.type == SAI_ROUTER_INTERFACE_TYPE_VLAN) {
            t.vlan = read(rif_api->get_router_interface_attribute, a.rif, SAI_ROUTER_INTERFACE_ATTR_VLAN_ID).oid;
            identity(t.vlan, SAI_OBJECT_TYPE_VLAN);
            t.vid = read(vlan_api->get_vlan_attribute, t.vlan, SAI_VLAN_ATTR_VLAN_ID).u16;
            require(t.vid >= 1 && t.vid <= 4094, "invalid VLAN ID");
            sai_object_id_t members[2]{}; sai_attribute_t list{};
            list.id = SAI_VLAN_ATTR_MEMBER_LIST; list.value.objlist.count = 2; list.value.objlist.list = members;
            check(vlan_api->get_vlan_attribute(t.vlan, 1, &list), "get bounded VLAN members (requires exactly one)");
            require(list.value.objlist.count == 1, "VLAN must have exactly one access member");
            t.member = members[0]; identity(t.member, SAI_OBJECT_TYPE_VLAN_MEMBER);
            require(read(vlan_api->get_vlan_member_attribute, t.member, SAI_VLAN_MEMBER_ATTR_VLAN_ID).oid == t.vlan, "VLAN member attachment mismatch");
            require(read(vlan_api->get_vlan_member_attribute, t.member, SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE).s32 == SAI_VLAN_TAGGING_MODE_UNTAGGED, "VLAN member must be untagged");
            t.bridge_port = read(vlan_api->get_vlan_member_attribute, t.member, SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID).oid;
            identity(t.bridge_port, SAI_OBJECT_TYPE_BRIDGE_PORT);
            require(read(bridge_api->get_bridge_port_attribute, t.bridge_port, SAI_BRIDGE_PORT_ATTR_TYPE).s32 == SAI_BRIDGE_PORT_TYPE_PORT, "unsupported bridge port type");
            require(read(bridge_api->get_bridge_port_attribute, t.bridge_port, SAI_BRIDGE_PORT_ATTR_PORT_ID).oid == a.port, "access bridge port attachment mismatch");
            t.bridge = read(bridge_api->get_bridge_port_attribute, t.bridge_port, SAI_BRIDGE_PORT_ATTR_BRIDGE_ID).oid;
            identity(t.bridge, SAI_OBJECT_TYPE_BRIDGE);
            require(read(bridge_api->get_bridge_attribute, t.bridge, SAI_BRIDGE_ATTR_TYPE).s32 == SAI_BRIDGE_TYPE_1Q, "only 1Q bridge supported");
            require(read(port_api->get_port_attribute, a.port, SAI_PORT_ATTR_PORT_VLAN_ID).u16 == t.vid, "port PVID does not match access VLAN");
        } else fail(SAI_STATUS_NOT_SUPPORTED, "only single-access-port VLAN or direct port RIF supported");
        return t;
    }
    void record_error(const Error& e) { ++stats.errors; stats.last_status = e.status; stats.last_error = e.what(); }
    bool residual() const { return stats.trap_group || stats.traps[0] || stats.traps[1] || stats.tables[0] || stats.tables[1]; }
    // Always preserve dependencies when removal fails, and continue independent cleanup.
    void cleanup() {
        sai_status_t first = SAI_STATUS_SUCCESS; std::string errors;
        auto erase = [&](sai_object_id_t& id, sai_remove_hostif_trap_fn fn, const char* name) {
            if (!id) return;
            sai_status_t s = fn(id);
            if (s == SAI_STATUS_SUCCESS) id = 0;
            else { if (first == SAI_STATUS_SUCCESS) first = s; errors += std::string(name) + " " + hex(id) + " status=" + std::to_string(s) + "; "; }
        };
        if (hostif) {
            for (int i = 1; i >= 0; --i) {
                erase(stats.tables[i], hostif->remove_hostif_table_entry, "remove hostif table");
                if (!stats.tables[i]) erase(stats.traps[i], hostif->remove_hostif_trap, "remove trap");
            }
            if (!stats.traps[0] && !stats.traps[1]) erase(stats.trap_group, hostif->remove_hostif_trap_group, "remove trap group");
        }
        if (first != SAI_STATUS_SUCCESS) fail(first, errors);
    }
    void capability(sai_object_type_t type, sai_attr_id_t attr, int32_t value) {
        int32_t values[128]{}; sai_s32_list_t list{}; list.count = 128; list.list = values;
        check(sdk.enum_values(sw, type, attr, &list), "query required hostif enum capability");
        if (list.count > 128 || std::find(values, values + list.count, value) == values + list.count)
            fail(SAI_STATUS_NOT_SUPPORTED, "required CB/COPY/trap/bypass capability unavailable");
    }
    void setup() {
        hostif = api<sai_hostif_api_t>(SAI_API_HOSTIF); switch_api = api<sai_switch_api_t>(SAI_API_SWITCH);
        rif_api = api<sai_router_interface_api_t>(SAI_API_ROUTER_INTERFACE); vlan_api = api<sai_vlan_api_t>(SAI_API_VLAN);
        bridge_api = api<sai_bridge_api_t>(SAI_API_BRIDGE); port_api = api<sai_port_api_t>(SAI_API_PORT);
        if (!hostif->create_hostif_trap_group || !hostif->remove_hostif_trap_group ||
            !hostif->create_hostif_trap || !hostif->remove_hostif_trap || !hostif->get_hostif_trap_attribute ||
            !hostif->create_hostif_table_entry || !hostif->remove_hostif_table_entry || !hostif->send_hostif_packet ||
            !switch_api->get_switch_attribute || !rif_api->get_router_interface_attribute || !vlan_api->get_vlan_attribute ||
            !vlan_api->get_vlan_member_attribute || !bridge_api->get_bridge_port_attribute || !bridge_api->get_bridge_attribute || !port_api->get_port_attribute)
            fail(SAI_STATUS_NOT_SUPPORTED, "required SAI hostif/topology functions unavailable");
        identity(sw, SAI_OBJECT_TYPE_SWITCH);
        require(read(switch_api->get_switch_attribute, sw, SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY).ptr ==
                reinterpret_cast<sai_pointer_t>(packet_callback()), "packet callback not registered (or owned by another consumer)");
        const int32_t types[2] = {SAI_HOSTIF_TRAP_TYPE_ARP_REQUEST, SAI_HOSTIF_TRAP_TYPE_IPV6_NEIGHBOR_DISCOVERY};
        capability(SAI_OBJECT_TYPE_HOSTIF_TABLE_ENTRY, SAI_HOSTIF_TABLE_ENTRY_ATTR_CHANNEL_TYPE, SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_CB);
        capability(SAI_OBJECT_TYPE_HOSTIF_TRAP, SAI_HOSTIF_TRAP_ATTR_PACKET_ACTION, SAI_PACKET_ACTION_COPY);
        capability(SAI_OBJECT_TYPE_HOSTIF_TRAP, SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE, types[0]);
        capability(SAI_OBJECT_TYPE_HOSTIF_TRAP, SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE, types[1]);
        capability(SAI_OBJECT_TYPE_HOSTIF_PACKET, SAI_HOSTIF_PACKET_ATTR_HOSTIF_TX_TYPE, SAI_HOSTIF_TX_TYPE_PIPELINE_BYPASS);
        std::array<sai_object_key_t, 512> existing{}; uint32_t count = existing.size();
        check(sdk.keys(sw, SAI_OBJECT_TYPE_HOSTIF_TRAP, &count, existing.data()), "enumerate existing traps (bounded 512; cannot safely claim ownership otherwise)");
        require(count <= existing.size(), "invalid trap enumeration count");
        for (uint32_t i = 0; i < count; ++i) {
            auto type = read(hostif->get_hostif_trap_attribute, existing[i].key.object_id, SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE).s32;
            if (type == types[0] || type == types[1]) fail(SAI_STATUS_ITEM_ALREADY_EXISTS, "ARP/ND trap already exists; refusing to steal it");
        }
        if (options.policer) identity(options.policer, SAI_OBJECT_TYPE_POLICER);
        sai_attribute_t group[2]{}; group[0].id = SAI_HOSTIF_TRAP_GROUP_ATTR_QUEUE; group[0].value.u32 = 0;
        group[1].id = SAI_HOSTIF_TRAP_GROUP_ATTR_POLICER; group[1].value.oid = options.policer;
        sai_object_id_t id = 0;
        check(hostif->create_hostif_trap_group(&id, sw, options.policer ? 2 : 1, group), "create responder trap group");
        stats.trap_group = id; require(id != 0, "SDK returned null trap group on success");
        for (size_t i = 0; i < 2; ++i) {
            sai_attribute_t a[3]{};
            a[0].id = SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE; a[0].value.s32 = types[i];
            a[1].id = SAI_HOSTIF_TRAP_ATTR_PACKET_ACTION; a[1].value.s32 = SAI_PACKET_ACTION_COPY;
            a[2].id = SAI_HOSTIF_TRAP_ATTR_TRAP_GROUP; a[2].value.oid = stats.trap_group;
            id = 0; check(hostif->create_hostif_trap(&id, sw, 3, a), "create responder COPY trap");
            stats.traps[i] = id; require(id != 0, "SDK returned null trap on success");
            require(read(hostif->get_hostif_trap_attribute, id, SAI_HOSTIF_TRAP_ATTR_PACKET_ACTION).s32 == SAI_PACKET_ACTION_COPY &&
                    read(hostif->get_hostif_trap_attribute, id, SAI_HOSTIF_TRAP_ATTR_TRAP_GROUP).oid == stats.trap_group,
                    "SDK trap COPY/group readback mismatch");
            a[0].id = SAI_HOSTIF_TABLE_ENTRY_ATTR_TYPE; a[0].value.s32 = SAI_HOSTIF_TABLE_ENTRY_TYPE_TRAP_ID;
            a[1].id = SAI_HOSTIF_TABLE_ENTRY_ATTR_TRAP_ID; a[1].value.oid = id;
            a[2].id = SAI_HOSTIF_TABLE_ENTRY_ATTR_CHANNEL_TYPE; a[2].value.s32 = SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_CB;
            id = 0; check(hostif->create_hostif_table_entry(&id, sw, 3, a), "create per-trap CB table");
            stats.tables[i] = id; require(id != 0, "SDK returned null table on success");
        }
    }
    void work() noexcept;
};
Service& service() { static Service s; return s; }

void callback(sai_object_id_t sw, sai_size_t n, const void* data, uint32_t count, const sai_attribute_t* attrs) noexcept {
    // No SDK calls, dynamic allocation, parsing or waiting on worker/control locks.
    // try_lock prevents callback-induced deadlocks even when SDK invokes inline.
    Service& s = service();
    try {
        if (!data || n < 14 || n > max_packet || !attrs || count > 16) { ++s.dropped; return; }
        sai_object_id_t port = 0, trap = 0; bool saw_port = false, saw_trap = false, saw_lag = false;
        for (uint32_t i = 0; i < count; ++i) {
            if (attrs[i].id == SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT) {
                if (saw_port) { ++s.dropped; return; } saw_port = true; port = attrs[i].value.oid;
            } else if (attrs[i].id == SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID) {
                if (saw_trap) { ++s.dropped; return; } saw_trap = true; trap = attrs[i].value.oid;
            } else if (attrs[i].id == SAI_HOSTIF_PACKET_ATTR_INGRESS_LAG) {
                if (saw_lag || attrs[i].value.oid) { ++s.dropped; return; } saw_lag = true;
            }
        }
        if (!port || !trap) { ++s.dropped; return; }
        std::unique_lock<std::mutex> l(s.queue_mutex, std::try_to_lock);
        if (!l.owns_lock()) { ++s.dropped; return; }
        if (!s.accepting || sw != s.sw || s.used == queue_capacity) { ++s.dropped; return; }
        auto now = Clock::now();
        if (now - s.window >= std::chrono::seconds(1)) { s.window = now; s.window_packets = 0; }
        if (s.window_packets >= packets_per_second) { ++s.dropped; return; }
        ++s.window_packets;
        Packet& p = s.queue[(s.head + s.used) % queue_capacity];
        std::memcpy(p.data.data(), data, n); p.size = n; p.port = port; p.trap = trap; p.generation = s.generation.load();
        ++s.used; ++s.admitted;
        l.unlock(); s.wake.notify_one();
    } catch (...) { ++s.dropped; } // Never unwind through the SDK C ABI.
}
void Service::work() noexcept {
    for (;;) {
        Packet p;
        {
            std::unique_lock<std::mutex> q(queue_mutex);
            wake.wait(q, [&] { return quitting || used; });
            if (quitting) return;
            p = queue[head]; head = (head + 1) % queue_capacity; --used;
        }
        std::lock_guard<std::mutex> c(control);
        if (!running || p.generation != generation.load()) continue;
        try {
            std::lock_guard<std::mutex> hardware(*sai_mutex);
            bool replied = false;
            for (const auto& item : records) {
                const Record& r = item.second; const Address& a = r.address;
                if (a.port != p.port || p.trap != stats.traps[a.target.ipv6 ? 1 : 0]) continue;
                auto reply = make_reply(a.target, p.data.data(), p.size);
                if (reply.empty()) continue;
                // Validate immediately before TX under the same shared SAI lock.
                require(validate(a) == r.attachment, "stale RIF MAC/attachment; remove and recreate address");
                sai_attribute_t out[2]{};
                out[0].id = SAI_HOSTIF_PACKET_ATTR_HOSTIF_TX_TYPE; out[0].value.s32 = SAI_HOSTIF_TX_TYPE_PIPELINE_BYPASS;
                out[1].id = SAI_HOSTIF_PACKET_ATTR_EGRESS_PORT_OR_LAG; out[1].value.oid = p.port;
                check(hostif->send_hostif_packet(sw, reply.size(), reply.data(), 2, out), "send_hostif_packet responder reply");
                ++stats.sent; replied = true; break;
            }
            if (!replied) ++stats.rejected;
        } catch (const Error& e) {
            record_error(e);
            // Stale topology is rejected per packet. SDK failures, including an
            // advertised but unsupported TX operation, fault the service and
            // propagate through subsequent CRUD/inventory instead of claiming
            // operational success. stop() still owns join and residual cleanup.
            if (e.status != SAI_STATUS_INVALID_PARAMETER) {
                running = false; faulted = true;
                std::lock_guard<std::mutex> q(queue_mutex);
                accepting = false; quitting = true; used = 0;
                return;
            }
        }
          catch (const std::exception& e) { record_error(Error(SAI_STATUS_FAILURE, e.what())); }
          catch (...) { record_error(Error(SAI_STATUS_FAILURE, "unexpected responder worker error")); }
    }
}
void active(Service& s, sai_object_id_t sw) {
    if (s.faulted)
        fail(s.stats.last_status, "interface-address responder faulted: " + s.stats.last_error);
    if (!s.running || sw != s.sw) fail(SAI_STATUS_NOT_SUPPORTED, "interface-address responder disabled/not started for this switch");
}
Observation observation(const Record& r) {
    Observation o; o.key = r.address.key;
    o.attributes = {{"router_interface", hex(r.address.rif)}, {"address", r.address.cidr}, {"ingress_port", hex(r.address.port)},
        {"mac", mactext(r.address.target.mac)}, {"state", "configured"}, {"observation_source", "software-responder"},
        {"dad", r.address.target.ipv6 ? "static-no-dad" : "not-applicable"}, {"neighbor_learning", "unsupported"}};
    return o;
}
} // namespace

sai_packet_event_notification_fn packet_callback() noexcept { (void)service(); return &callback; }
void start(sai_object_id_t sw, const Options& options, const Sdk& sdk, std::mutex& sai_mutex) {
    Service& s = service(); std::lock_guard<std::mutex> lifecycle(s.lifecycle); std::lock_guard<std::mutex> c(s.control);
    if (s.running || s.worker.joinable() || s.residual()) fail(SAI_STATUS_OBJECT_IN_USE, "responder already started or cleanup pending");
    if (!options.enabled) return;
    require(sw != 0, "null switch");
    if (!sdk.query || !sdk.keys || !sdk.object_type || !sdk.switch_id || !sdk.enum_values) fail(SAI_STATUS_NOT_SUPPORTED, "required SAI enumeration/identity/capability entrypoints unavailable");
    require(options.policer || options.allow_unpoliced_cpu, "supply hardware policer or explicitly allow software-bounded CPU handling");
    s.sdk = sdk; s.options = options; s.sai_mutex = &sai_mutex;
    { std::lock_guard<std::mutex> q(s.queue_mutex); s.sw = sw; s.used = 0; s.head = 0; s.quitting = false; s.accepting = false; }
    std::lock_guard<std::mutex> hardware(sai_mutex);
    try {
        s.setup();
        s.running = true; s.faulted = false; ++s.generation;
        s.stats.last_status = SAI_STATUS_SUCCESS; s.stats.last_error.clear();
        { std::lock_guard<std::mutex> q(s.queue_mutex); s.accepting = true; s.window = Clock::now(); s.window_packets = 0; }
        // Last potentially throwing operation; no started worker is abandoned on rollback.
        s.worker = std::thread([&s] { s.work(); });
    } catch (const std::exception& e) {
        s.running = false;
        { std::lock_guard<std::mutex> q(s.queue_mutex); s.accepting = false; s.quitting = true; s.used = 0; }
        const Error* error = dynamic_cast<const Error*>(&e);
        const sai_status_t code = error ? error->status : SAI_STATUS_FAILURE;
        std::string message = e.what();
        try { s.cleanup(); } catch (const Error& cleanup) { message += "; rollback incomplete: "; message += cleanup.what(); }
        Error result(code, message); s.record_error(result); throw result;
    }
}
void stop() {
    Service& s = service(); std::lock_guard<std::mutex> lifecycle(s.lifecycle);
    {
        // Admission off first; do not wait for worker with either lock held.
        std::lock_guard<std::mutex> q(s.queue_mutex); s.accepting = false; s.quitting = true; s.used = 0; ++s.generation;
    }
    s.wake.notify_all();
    if (s.worker.joinable()) s.worker.join();
    std::lock_guard<std::mutex> c(s.control); s.running = false; s.faulted = false; s.records.clear();
    if (s.residual()) {
        std::lock_guard<std::mutex> hardware(*s.sai_mutex);
        try { s.cleanup(); } catch (const Error& e) { s.record_error(e); throw; }
    }
}
Observation create(sai_object_id_t sw, const Attributes& attrs) {
    Service& s = service(); std::lock_guard<std::mutex> c(s.control); active(s, sw);
    require(attrs.size() == 3 && attrs.count("router_interface") && attrs.count("address") && attrs.count("ingress_port"), "create requires exactly router_interface,address,ingress_port");
    Address a = parse(oid(attrs.at("router_interface")), attrs.at("address")); a.port = oid(attrs.at("ingress_port"));
    if (a.target.ipv6 && !s.options.static_ipv6_no_dad) fail(SAI_STATUS_NOT_SUPPORTED, "IPv6 requires explicit static-no-DAD opt-in and operator-guaranteed uniqueness");
    if (s.records.count(a.key)) fail(SAI_STATUS_ITEM_ALREADY_EXISTS, "interface address exists");
    require(s.records.size() < max_addresses, "responder address limit reached (256)");
    for (const auto& item : s.records) {
        const Address& other = item.second.address;
        require((other.port != a.port || other.rif == a.rif) && (other.rif != a.rif || other.port == a.port), "ambiguous ingress/RIF mapping");
        require(!(other.port == a.port && other.target.ipv6 == a.target.ipv6 && other.target.ip == a.target.ip), "same host IP already configured on this ingress (different prefix)");
    }
    std::lock_guard<std::mutex> hardware(*s.sai_mutex);
    Record r; r.address = a; r.attachment = s.validate(a); r.address.target.mac = r.attachment.mac;
    // Different families/aliases on one RIF must share the same validated attachment.
    for (const auto& item : s.records) if (item.second.address.rif == a.rif)
        require(item.second.attachment == r.attachment, "existing RIF address attachment is stale");
    Observation result = observation(r); s.records.emplace(a.key, r); ++s.generation;
    return result;
}
Observation get(sai_object_id_t sw, const std::string& text) {
    Service& s = service(); std::lock_guard<std::mutex> c(s.control); active(s, sw);
    auto it = s.records.find(key(text).key); if (it == s.records.end()) fail(SAI_STATUS_ITEM_NOT_FOUND, "interface address not found");
    std::lock_guard<std::mutex> hardware(*s.sai_mutex);
    require(s.validate(it->second.address) == it->second.attachment, "stale RIF MAC/attachment; remove and recreate address");
    return observation(it->second);
}
void remove(sai_object_id_t sw, const std::string& text) {
    Service& s = service(); std::lock_guard<std::mutex> c(s.control);
    // Removal only drops software state, so it stays available after a fault:
    // otherwise mutation_guard() would lock out topology repair until restart.
    if (!s.faulted || sw != s.sw) active(s, sw);
    if (!s.records.erase(key(text).key)) fail(SAI_STATUS_ITEM_NOT_FOUND, "interface address not found");
    ++s.generation;
}
std::vector<Observation> list(sai_object_id_t sw) {
    Service& s = service(); std::lock_guard<std::mutex> c(s.control);
    if (!s.running && !s.faulted) return {};
    active(s, sw); std::lock_guard<std::mutex> hardware(*s.sai_mutex); std::vector<Observation> out;
    for (const auto& item : s.records) {
        require(s.validate(item.second.address) == item.second.attachment, "stale RIF MAC/attachment in service inventory");
        out.push_back(observation(item.second));
    }
    return out;
}
Status status() {
    Service& s = service(); std::lock_guard<std::mutex> c(s.control); std::lock_guard<std::mutex> q(s.queue_mutex);
    Status result = s.stats; result.running = s.running; result.addresses = s.records.size(); result.queued = s.used;
    result.dropped = s.dropped.load(); result.admitted = s.admitted.load(); return result;
}

std::vector<uint8_t> make_reply(const Target& t, const uint8_t* p, size_t n) {
    if (!p || n < 14 || n > max_packet || !unicast_mac(t.mac.data()) || !unicast_mac(p + 6) || equal(p + 6, t.mac.data(), 6)) return {};
    const uint8_t broadcast[6] = {255,255,255,255,255,255};
    if (!t.ipv6) {
        if (be16(p + 12) != 0x0806 || n < 42 || (!equal(p, broadcast, 6) && !equal(p, t.mac.data(), 6))) return {};
        const uint8_t* a = p + 14;
        if (be16(a) != 1 || be16(a + 2) != 0x0800 || a[4] != 6 || a[5] != 4 || be16(a + 6) != 1 ||
            !equal(a + 8, p + 6, 6) || !equal(a + 24, t.ip.data(), 4) || a[14] >= 224 || a[14] == 127 ||
            equal(a + 14, t.ip.data(), 4)) return {};
        std::vector<uint8_t> out(60, 0); // Ethernet minimum without FCS.
        std::copy(p + 6, p + 12, out.begin()); std::copy(t.mac.begin(), t.mac.end(), out.begin() + 6); put16(out.data() + 12, 0x0806);
        uint8_t* r = out.data() + 14; put16(r, 1); put16(r + 2, 0x0800); r[4] = 6; r[5] = 4; put16(r + 6, 2);
        std::copy(t.mac.begin(), t.mac.end(), r + 8); std::copy(t.ip.begin(), t.ip.begin() + 4, r + 14);
        std::copy(p + 6, p + 12, r + 18); std::copy(a + 14, a + 18, r + 24); return out;
    }
    if (be16(p + 12) != 0x86dd || n < 78) return {};
    const uint8_t* ip = p + 14; const uint8_t* ns = ip + 40; size_t len = be16(ip + 4);
    // Reject ALL extensions (including fragment/atomic fragment) rather than
    // attempting an ambiguous/unbounded extension-header traversal.
    if ((ip[0] >> 4) != 6 || ip[6] != 58 || ip[7] != 255 || len < 24 || len > 256 || n < 54 + len ||
        ns[0] != 135 || ns[1] != 0 || !equal(ns + 8, t.ip.data(), 16) || t.ip[0] == 255 ||
        ip[8] == 255 || equal(ip + 8, t.ip.data(), 16) || icmp_checksum(ip, len) != 0) return {};
    bool dad = zero(ip + 8, 16);
    if (!ipv6_unicast(t.ip.data()) || (!dad && !ipv6_unicast(ip + 8))) return {};
    uint8_t solicited[16] = {0xff,0x02,0,0,0,0,0,0,0,0,0,1,0xff,0,0,0};
    std::copy(t.ip.begin() + 13, t.ip.end(), solicited + 13);
    bool multicast = equal(ip + 24, solicited, 16);
    if ((!multicast && !equal(ip + 24, t.ip.data(), 16)) || (dad && !multicast)) return {};
    if (multicast) {
        uint8_t dest[6] = {0x33,0x33,0xff,t.ip[13],t.ip[14],t.ip[15]};
        if (!equal(p, dest, 6)) return {};
    } else if (!equal(p, t.mac.data(), 6)) return {};
    bool slla = false; unsigned options = 0;
    for (size_t pos = 24; pos < len;) {
        if (++options > 16 || len - pos < 2 || ns[pos + 1] == 0) return {};
        size_t size = size_t(ns[pos + 1]) * 8; if (size > len - pos) return {};
        if (ns[pos] == 1) {
            if (dad || slla || size != 8 || !equal(ns + pos + 2, p + 6, 6)) return {};
            slla = true;
        }
        pos += size;
    }
    std::vector<uint8_t> out(86, 0); uint8_t* r = out.data() + 14;
    std::copy(t.mac.begin(), t.mac.end(), out.begin() + 6); put16(out.data() + 12, 0x86dd);
    r[0] = 0x60; put16(r + 4, 32); r[6] = 58; r[7] = 255; std::copy(t.ip.begin(), t.ip.end(), r + 8);
    if (dad) {
        const uint8_t allnodes[16] = {0xff,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1};
        const uint8_t eth[6] = {0x33,0x33,0,0,0,1};
        std::copy(allnodes, allnodes + 16, r + 24); std::copy(eth, eth + 6, out.begin());
    } else { std::copy(ip + 8, ip + 24, r + 24); std::copy(p + 6, p + 12, out.begin()); }
    uint8_t* na = r + 40; na[0] = 136; na[4] = dad ? 0xa0 : 0xe0; // Router, Solicited (except DAD), Override.
    std::copy(t.ip.begin(), t.ip.end(), na + 8); na[24] = 2; na[25] = 1; std::copy(t.mac.begin(), t.mac.end(), na + 26);
    put16(na + 2, icmp_checksum(r, 32)); return out;
}
} // namespace interface_address
