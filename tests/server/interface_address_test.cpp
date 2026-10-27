#include "interface_address.h"
#include <arpa/inet.h>
#include <algorithm>
#include <atomic>
#include <cassert>
#include <chrono>
#include <condition_variable>
#include <cstring>
#include <functional>
#include <iostream>
#include <map>
#include <thread>

namespace ia = interface_address;
namespace {
const sai_object_id_t sw = 1;
std::mutex hardware;
const std::array<uint8_t, 6> router{{2,0,0,0,4,1}}, client{{2,3,4,5,6,7}};
using Bytes = std::vector<uint8_t>;
void put16(Bytes& p, size_t off, unsigned n) { p.at(off) = uint8_t(n >> 8); p.at(off + 1) = uint8_t(n); }
unsigned be16(const Bytes& p, size_t off) { return (unsigned(p.at(off)) << 8) | p.at(off + 1); }
// Independent checksum calculation over concatenated pseudo-header and ICMP data.
unsigned checksum(const Bytes& p) {
    Bytes bytes(p.begin() + 22, p.begin() + 54);
    const unsigned len = be16(p, 18);
    bytes.insert(bytes.end(), {0, 0, uint8_t(len >> 8), uint8_t(len), 0, 0, 0, 58});
    bytes.insert(bytes.end(), p.begin() + 54, p.begin() + 54 + len);
    if (bytes.size() % 2) bytes.push_back(0);
    unsigned s = 0;
    for (size_t i = 0; i < bytes.size(); i += 2) s += be16(bytes, i);
    while (s > 65535) s = (s & 65535) + (s >> 16);
    return (~s) & 65535;
}
void fix_checksum(Bytes& p) { put16(p, 56, 0); put16(p, 56, checksum(p)); }
ia::Target target(const char* ip) {
    ia::Target t; t.mac = router; t.ipv6 = std::strchr(ip, ':') != nullptr;
    assert(inet_pton(t.ipv6 ? AF_INET6 : AF_INET, ip, t.ip.data()) == 1); return t;
}
Bytes arp(const ia::Target& t) {
    Bytes p(60, 0); std::fill(p.begin(), p.begin() + 6, 255); std::copy(client.begin(), client.end(), p.begin() + 6);
    put16(p, 12, 0x0806); put16(p, 14, 1); put16(p, 16, 0x0800); p[18] = 6; p[19] = 4; put16(p, 20, 1);
    std::copy(client.begin(), client.end(), p.begin() + 22); p[28] = 192; p[29] = 0; p[30] = 2; p[31] = 2;
    std::copy(t.ip.begin(), t.ip.begin() + 4, p.begin() + 38); return p;
}
Bytes ns(const ia::Target& t, bool dad = false, bool slla = true) {
    Bytes p(slla ? 86 : 78, 0); p[0] = p[1] = 0x33; p[2] = 0xff;
    std::copy(t.ip.begin() + 13, t.ip.end(), p.begin() + 3); std::copy(client.begin(), client.end(), p.begin() + 6);
    put16(p, 12, 0x86dd); p[14] = 0x60; put16(p, 18, slla ? 32 : 24); p[20] = 58; p[21] = 255;
    if (!dad) assert(inet_pton(AF_INET6, "fe80::203:405:607", p.data() + 22) == 1);
    assert(inet_pton(AF_INET6, "ff02::1:ff00:0", p.data() + 38) == 1);
    std::copy(t.ip.begin() + 13, t.ip.end(), p.begin() + 51); p[54] = 135;
    std::copy(t.ip.begin(), t.ip.end(), p.begin() + 62);
    if (slla) { p[78] = 1; p[79] = 1; std::copy(client.begin(), client.end(), p.begin() + 80); }
    fix_checksum(p); return p;
}
Bytes reply(const ia::Target& t, const Bytes& p) { return ia::make_reply(t, p.data(), p.size()); }
void packet_tests() {
    auto v4 = target("192.0.2.1"), v6 = target("2001:db8:101::1");
    Bytes p = arp(v4); auto r = reply(v4, p);
    assert(r.size() == 60 && be16(r, 20) == 2);
    assert(std::equal(client.begin(), client.end(), r.begin()));
    assert(std::equal(router.begin(), router.end(), r.begin() + 6));
    assert(std::equal(v4.ip.begin(), v4.ip.begin() + 4, r.begin() + 28));
    assert(std::equal(p.begin() + 28, p.begin() + 32, r.begin() + 38));
    for (size_t off : {size_t(12), size_t(14), size_t(16), size_t(18), size_t(19), size_t(20), size_t(22), size_t(38)}) {
        auto bad = p; bad[off] ^= 1; assert(reply(v4, bad).empty());
    }
    for (size_t n = 0; n < 42; ++n) assert(ia::make_reply(v4, p.data(), n).empty());
    auto bad = p; bad[6] |= 1; assert(reply(v4, bad).empty());
    bad = p; std::fill(bad.begin() + 6, bad.begin() + 12, 0); assert(reply(v4, bad).empty());
    bad = p; bad[0] = 2; assert(reply(v4, bad).empty());
    bad = p; put16(bad, 12, 0x8100); assert(reply(v4, bad).empty());
    bad = p; bad.resize(2049); assert(reply(v4, bad).empty());
    bad = p; std::fill(bad.begin() + 28, bad.begin() + 32, 0); assert(!reply(v4, bad).empty()); // ARP probe.
    p = ns(v6); r = reply(v6, p);
    assert(r.size() == 86 && r[54] == 136 && r[58] == 0xe0 && r[21] == 255 && checksum(r) == 0);
    assert(std::equal(v6.ip.begin(), v6.ip.end(), r.begin() + 22));
    assert(std::equal(p.begin() + 22, p.begin() + 38, r.begin() + 38));
    assert(r[78] == 2 && r[79] == 1 && std::equal(router.begin(), router.end(), r.begin() + 80));
    // Ordinary unicast NS also works and missing SLLA is permitted.
    auto unicast = p; std::copy(v6.ip.begin(), v6.ip.end(), unicast.begin() + 38);
    std::copy(router.begin(), router.end(), unicast.begin()); fix_checksum(unicast); assert(!reply(v6, unicast).empty());
    assert(!reply(v6, ns(v6, false, false)).empty());
    for (size_t n = 0; n < p.size(); ++n) assert(ia::make_reply(v6, p.data(), n).empty());
    for (size_t off : {size_t(0), size_t(12), size_t(18), size_t(20), size_t(21), size_t(54), size_t(55), size_t(56), size_t(62), size_t(79), size_t(80)}) {
        bad = p; bad[off] ^= 1; assert(reply(v6, bad).empty());
    }
    bad = p; bad[14] = 0x40; assert(reply(v6, bad).empty());
    bad = p; bad[20] = 44; assert(reply(v6, bad).empty()); // No atomic or ordinary fragments.
    bad = p; bad[20] = 0; assert(reply(v6, bad).empty()); // No extension traversal.
    bad = p; bad[79] = 0; fix_checksum(bad); assert(reply(v6, bad).empty());
    bad = p; bad[79] = 2; fix_checksum(bad); assert(reply(v6, bad).empty());
    bad = p; bad[80] ^= 2; fix_checksum(bad); assert(reply(v6, bad).empty()); // SLLA vs Ethernet.
    bad = p; bad[22] = 255; fix_checksum(bad); assert(reply(v6, bad).empty());
    bad = p; assert(inet_pton(AF_INET6, "::1", bad.data() + 22) == 1); fix_checksum(bad); assert(reply(v6, bad).empty());
    bad = p; assert(inet_pton(AF_INET6, "::ffff:192.0.2.1", bad.data() + 22) == 1); fix_checksum(bad); assert(reply(v6, bad).empty());
    bad = p; bad[38] ^= 1; fix_checksum(bad); assert(reply(v6, bad).empty());
    bad = p; bad.insert(bad.end(), p.begin() + 78, p.end()); put16(bad, 18, 40); fix_checksum(bad); assert(reply(v6, bad).empty()); // Duplicate SLLA.
    bad = p; bad[78] = 99; fix_checksum(bad); assert(!reply(v6, bad).empty()); // Unknown bounded options skipped.
    bad = p; bad.resize(54 + 25); put16(bad, 18, 25); fix_checksum(bad); assert(reply(v6, bad).empty());
    p = ns(v6, true, false); r = reply(v6, p);
    assert(r.size() == 86 && r[58] == 0xa0 && checksum(r) == 0);
    const uint8_t eth[] = {0x33,0x33,0,0,0,1}; assert(std::equal(eth, eth + 6, r.begin()));
    assert(r[38] == 255 && r[39] == 2 && r[53] == 1);
    assert(reply(v6, ns(v6, true, true)).empty()); // DAD forbids any SLLA.
    bad = p; std::copy(v6.ip.begin(), v6.ip.end(), bad.begin() + 38);
    std::copy(router.begin(), router.end(), bad.begin()); fix_checksum(bad); assert(reply(v6, bad).empty());
    // Deterministic malformed-packet sweep for length/option/checksum boundaries.
    uint32_t seed = 12345;
    for (unsigned i = 0; i < 5000; ++i) {
        seed = seed * 1664525 + 1013904223; bad = ns(v6); bad[seed % bad.size()] ^= uint8_t(seed >> 16);
        (void)reply(v6, bad);
    }
}
struct Node { sai_object_type_t type; std::map<sai_attr_id_t, sai_attribute_value_t> attrs; };
struct Fake {
    std::map<sai_object_id_t, Node> nodes;
    sai_hostif_api_t hostif{}; sai_switch_api_t switch_api{}; sai_router_interface_api_t rif{};
    sai_vlan_api_t vlan{}; sai_bridge_api_t bridge{}; sai_port_api_t port{};
    sai_object_id_t next = 10000, fail_remove = 0, fail_get = 0;
    unsigned creates = 0, fail_create = 0, removes = 0;
    bool enumeration = true, capability = true, send_error = false;
    std::mutex sent_mutex;
    std::condition_variable sent_cv;
    std::vector<std::pair<sai_object_id_t, Bytes>> sent;
    bool hold_send = false, entered_send = false;
    void reset();
    void add(sai_object_id_t id, sai_object_type_t type) { nodes.emplace(id, Node{type, {}}); }
    void s32(sai_object_id_t id, sai_attr_id_t attr, int32_t n) { nodes.at(id).attrs[attr].s32 = n; }
    void oid(sai_object_id_t id, sai_attr_id_t attr, sai_object_id_t n) { nodes.at(id).attrs[attr].oid = n; }
    void u16(sai_object_id_t id, sai_attr_id_t attr, uint16_t n) { nodes.at(id).attrs[attr].u16 = n; }
    void flag(sai_object_id_t id, sai_attr_id_t attr, bool n) { nodes.at(id).attrs[attr].booldata = n; }
    void access(unsigned n);
    size_t owned() const {
        size_t result = 0; for (const auto& item : nodes) if (item.first >= 10000) ++result; return result;
    }
} f;
sai_status_t get_attr(sai_object_id_t id, uint32_t count, sai_attribute_t* attrs) {
    if (id == f.fail_get) return SAI_STATUS_FAILURE;
    auto it = f.nodes.find(id); if (it == f.nodes.end()) return SAI_STATUS_ITEM_NOT_FOUND;
    for (uint32_t i = 0; i < count; ++i) {
        if (it->second.type == SAI_OBJECT_TYPE_VLAN && attrs[i].id == SAI_VLAN_ATTR_MEMBER_LIST) {
            std::vector<sai_object_id_t> members;
            for (const auto& item : f.nodes) if (item.second.type == SAI_OBJECT_TYPE_VLAN_MEMBER &&
                item.second.attrs.at(SAI_VLAN_MEMBER_ATTR_VLAN_ID).oid == id) members.push_back(item.first);
            const auto capacity = attrs[i].value.objlist.count; attrs[i].value.objlist.count = members.size();
            if (capacity < members.size()) return SAI_STATUS_BUFFER_OVERFLOW;
            std::copy(members.begin(), members.end(), attrs[i].value.objlist.list);
        } else {
            auto attr = it->second.attrs.find(attrs[i].id); if (attr == it->second.attrs.end()) return SAI_STATUS_NOT_SUPPORTED;
            attrs[i].value = attr->second;
        }
    }
    return SAI_STATUS_SUCCESS;
}
sai_status_t add_node(sai_object_type_t type, sai_object_id_t* id, sai_object_id_t switch_id, uint32_t count, const sai_attribute_t* attrs) {
    assert(switch_id == sw); ++f.creates;
    if (f.creates == f.fail_create) { *id = 987654; return SAI_STATUS_FAILURE; } // Failure output is NOT owned.
    *id = f.next++; f.add(*id, type);
    for (uint32_t i = 0; i < count; ++i) f.nodes.at(*id).attrs[attrs[i].id] = attrs[i].value;
    if (type == SAI_OBJECT_TYPE_HOSTIF_TRAP) {
        assert(f.nodes.at(*id).attrs.at(SAI_HOSTIF_TRAP_ATTR_PACKET_ACTION).s32 == SAI_PACKET_ACTION_COPY);
        assert(f.nodes.count(f.nodes.at(*id).attrs.at(SAI_HOSTIF_TRAP_ATTR_TRAP_GROUP).oid));
    }
    if (type == SAI_OBJECT_TYPE_HOSTIF_TABLE_ENTRY) {
        assert(f.nodes.at(*id).attrs.at(SAI_HOSTIF_TABLE_ENTRY_ATTR_TYPE).s32 == SAI_HOSTIF_TABLE_ENTRY_TYPE_TRAP_ID);
        assert(f.nodes.at(*id).attrs.at(SAI_HOSTIF_TABLE_ENTRY_ATTR_CHANNEL_TYPE).s32 == SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_CB);
    }
    return SAI_STATUS_SUCCESS;
}
sai_status_t group_create(sai_object_id_t* id, sai_object_id_t s, uint32_t n, const sai_attribute_t* a) { return add_node(SAI_OBJECT_TYPE_HOSTIF_TRAP_GROUP, id, s, n, a); }
sai_status_t trap_create(sai_object_id_t* id, sai_object_id_t s, uint32_t n, const sai_attribute_t* a) { return add_node(SAI_OBJECT_TYPE_HOSTIF_TRAP, id, s, n, a); }
sai_status_t table_create(sai_object_id_t* id, sai_object_id_t s, uint32_t n, const sai_attribute_t* a) { return add_node(SAI_OBJECT_TYPE_HOSTIF_TABLE_ENTRY, id, s, n, a); }
sai_status_t erase(sai_object_id_t id) {
    ++f.removes; assert(f.nodes.count(id)); if (id == f.fail_remove) return SAI_STATUS_FAILURE;
    for (const auto& item : f.nodes) {
        if (item.second.type == SAI_OBJECT_TYPE_HOSTIF_TRAP) assert(item.second.attrs.at(SAI_HOSTIF_TRAP_ATTR_TRAP_GROUP).oid != id);
        if (item.second.type == SAI_OBJECT_TYPE_HOSTIF_TABLE_ENTRY) assert(item.second.attrs.at(SAI_HOSTIF_TABLE_ENTRY_ATTR_TRAP_ID).oid != id);
    }
    f.nodes.erase(id); return SAI_STATUS_SUCCESS;
}
sai_status_t send_packet(sai_object_id_t s, sai_size_t n, const void* data, uint32_t count, const sai_attribute_t* attrs) {
    assert(s == sw && count == 2);
    assert(attrs[0].id == SAI_HOSTIF_PACKET_ATTR_HOSTIF_TX_TYPE && attrs[0].value.s32 == SAI_HOSTIF_TX_TYPE_PIPELINE_BYPASS);
    assert(attrs[1].id == SAI_HOSTIF_PACKET_ATTR_EGRESS_PORT_OR_LAG);
    std::unique_lock<std::mutex> l(f.sent_mutex); f.entered_send = true; f.sent_cv.notify_all();
    assert(f.sent_cv.wait_for(l, std::chrono::seconds(3), [] { return !f.hold_send; }));
    if (f.send_error) return SAI_STATUS_NOT_SUPPORTED;
    const auto* bytes = static_cast<const uint8_t*>(data);
    f.sent.emplace_back(attrs[1].value.oid, Bytes(bytes, bytes + n)); f.sent_cv.notify_all(); return SAI_STATUS_SUCCESS;
}
sai_status_t query(sai_api_t api, void** out) {
    switch (api) {
    case SAI_API_HOSTIF: *out = &f.hostif; break;
    case SAI_API_SWITCH: *out = &f.switch_api; break;
    case SAI_API_ROUTER_INTERFACE: *out = &f.rif; break;
    case SAI_API_VLAN: *out = &f.vlan; break;
    case SAI_API_BRIDGE: *out = &f.bridge; break;
    case SAI_API_PORT: *out = &f.port; break;
    default: return SAI_STATUS_NOT_SUPPORTED;
    }
    return SAI_STATUS_SUCCESS;
}
sai_status_t keys(sai_object_id_t s, sai_object_type_t type, uint32_t* count, sai_object_key_t* out) {
    assert(s == sw && type == SAI_OBJECT_TYPE_HOSTIF_TRAP);
    if (!f.enumeration) return SAI_STATUS_NOT_SUPPORTED;
    std::vector<sai_object_id_t> ids;
    for (const auto& item : f.nodes) if (item.second.type == type) ids.push_back(item.first);
    auto capacity = *count; *count = ids.size(); if (capacity < ids.size()) return SAI_STATUS_BUFFER_OVERFLOW;
    for (size_t i = 0; i < ids.size(); ++i) out[i].key.object_id = ids[i];
    return SAI_STATUS_SUCCESS;
}
sai_object_type_t object_type(sai_object_id_t id) { auto it = f.nodes.find(id); return it == f.nodes.end() ? SAI_OBJECT_TYPE_NULL : it->second.type; }
sai_object_id_t switch_id(sai_object_id_t id) { return f.nodes.count(id) ? sw : 0; }
sai_status_t enum_values(sai_object_id_t s, sai_object_type_t type, sai_attr_id_t attr, sai_s32_list_t* values) {
    assert(s == sw && values->count >= 2); if (!f.capability) return SAI_STATUS_NOT_SUPPORTED;
    values->count = 1;
    if (type == SAI_OBJECT_TYPE_HOSTIF_TABLE_ENTRY && attr == SAI_HOSTIF_TABLE_ENTRY_ATTR_CHANNEL_TYPE) values->list[0] = SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_CB;
    else if (type == SAI_OBJECT_TYPE_HOSTIF_TRAP && attr == SAI_HOSTIF_TRAP_ATTR_PACKET_ACTION) values->list[0] = SAI_PACKET_ACTION_COPY;
    else if (type == SAI_OBJECT_TYPE_HOSTIF_TRAP && attr == SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE) {
        values->count = 2; values->list[0] = SAI_HOSTIF_TRAP_TYPE_ARP_REQUEST; values->list[1] = SAI_HOSTIF_TRAP_TYPE_IPV6_NEIGHBOR_DISCOVERY;
    } else {
        assert(type == SAI_OBJECT_TYPE_HOSTIF_PACKET && attr == SAI_HOSTIF_PACKET_ATTR_HOSTIF_TX_TYPE);
        values->list[0] = SAI_HOSTIF_TX_TYPE_PIPELINE_BYPASS;
    }
    return SAI_STATUS_SUCCESS;
}
void Fake::reset() {
    ia::stop(); assert(owned() == 0); nodes.clear(); creates = removes = fail_create = 0; fail_get = fail_remove = 0;
    enumeration = capability = true; send_error = false; sent.clear(); entered_send = hold_send = false; next = 10000;
    hostif = {}; switch_api = {}; rif = {}; vlan = {}; bridge = {}; port = {};
    hostif.create_hostif_trap_group = group_create; hostif.remove_hostif_trap_group = erase;
    hostif.create_hostif_trap = trap_create; hostif.remove_hostif_trap = erase; hostif.get_hostif_trap_attribute = get_attr;
    hostif.create_hostif_table_entry = table_create; hostif.remove_hostif_table_entry = erase; hostif.send_hostif_packet = send_packet;
    switch_api.get_switch_attribute = get_attr; rif.get_router_interface_attribute = get_attr; vlan.get_vlan_attribute = get_attr;
    vlan.get_vlan_member_attribute = get_attr; bridge.get_bridge_port_attribute = get_attr; bridge.get_bridge_attribute = get_attr; port.get_port_attribute = get_attr;
    add(sw, SAI_OBJECT_TYPE_SWITCH); nodes.at(sw).attrs[SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY].ptr = reinterpret_cast<sai_pointer_t>(ia::packet_callback());
    add(5000, SAI_OBJECT_TYPE_BRIDGE); s32(5000, SAI_BRIDGE_ATTR_TYPE, SAI_BRIDGE_TYPE_1Q);
}
void Fake::access(unsigned n) {
    const sai_object_id_t r = 1000 + n, p = 200 + n, v = 2000 + n, m = 3000 + n, bp = 4000 + n;
    add(r, SAI_OBJECT_TYPE_ROUTER_INTERFACE); s32(r, SAI_ROUTER_INTERFACE_ATTR_TYPE, SAI_ROUTER_INTERFACE_TYPE_VLAN);
    oid(r, SAI_ROUTER_INTERFACE_ATTR_VLAN_ID, v); flag(r, SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE, true); flag(r, SAI_ROUTER_INTERFACE_ATTR_ADMIN_V6_STATE, true);
    std::copy(router.begin(), router.end(), nodes.at(r).attrs[SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS].mac);
    add(p, SAI_OBJECT_TYPE_PORT); s32(p, SAI_PORT_ATTR_TYPE, SAI_PORT_TYPE_LOGICAL); u16(p, SAI_PORT_ATTR_PORT_VLAN_ID, 100 + n);
    add(v, SAI_OBJECT_TYPE_VLAN); u16(v, SAI_VLAN_ATTR_VLAN_ID, 100 + n);
    add(m, SAI_OBJECT_TYPE_VLAN_MEMBER); oid(m, SAI_VLAN_MEMBER_ATTR_VLAN_ID, v); oid(m, SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID, bp);
    s32(m, SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE, SAI_VLAN_TAGGING_MODE_UNTAGGED);
    add(bp, SAI_OBJECT_TYPE_BRIDGE_PORT); s32(bp, SAI_BRIDGE_PORT_ATTR_TYPE, SAI_BRIDGE_PORT_TYPE_PORT);
    oid(bp, SAI_BRIDGE_PORT_ATTR_PORT_ID, p); oid(bp, SAI_BRIDGE_PORT_ATTR_BRIDGE_ID, 5000);
}
ia::Sdk sdk() { ia::Sdk s; s.query = query; s.keys = keys; s.object_type = object_type; s.switch_id = switch_id; s.enum_values = enum_values; return s; }
ia::Options options() { ia::Options o; o.enabled = true; o.allow_unpoliced_cpu = true; o.static_ipv6_no_dad = true; return o; }
void start(const ia::Options& o = options()) { ia::start(sw, o, sdk(), hardware); }
ia::Attributes attrs(unsigned n, const std::string& ip = "192.0.2.1/24") {
    return {{"router_interface", std::to_string(1000 + n)}, {"ingress_port", std::to_string(200 + n)}, {"address", ip}};
}
void error(const std::function<void()>& call, sai_status_t expected = SAI_STATUS_SUCCESS) {
    bool caught = false;
    try { call(); } catch (const ia::Error& e) { caught = true; if (expected != SAI_STATUS_SUCCESS) assert(e.status == expected); }
    assert(caught);
}
void inject(const Bytes& p, sai_object_id_t port, sai_object_id_t trap, sai_object_id_t switch_oid = sw, bool lag = false) {
    sai_attribute_t a[3]{}; a[0].id = SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT; a[0].value.oid = port;
    a[1].id = SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID; a[1].value.oid = trap;
    a[2].id = SAI_HOSTIF_PACKET_ATTR_INGRESS_LAG; a[2].value.oid = lag ? 888 : 0;
    ia::packet_callback()(switch_oid, p.size(), p.data(), 3, a);
}
void inject_reliably(const Bytes& p, sai_object_id_t port, sai_object_id_t trap) {
    // The production callback intentionally drops on try_lock contention. Tests
    // expecting one processed packet must retry admission, not assume delivery.
    auto admitted = ia::status().admitted;
    for (unsigned attempt = 0; attempt < 10000; ++attempt) {
        inject(p, port, trap);
        if (ia::status().admitted > admitted) return;
        std::this_thread::yield();
    }
    assert(false && "test packet could not be admitted");
}
void wait_sent(size_t n) {
    std::unique_lock<std::mutex> l(f.sent_mutex);
    assert(f.sent_cv.wait_for(l, std::chrono::seconds(3), [&] { return f.sent.size() >= n; }));
}
void wait_stat(const std::function<bool(const ia::Status&)>& condition) {
    auto deadline = std::chrono::steady_clock::now() + std::chrono::seconds(3);
    while (!condition(ia::status())) {
        assert(std::chrono::steady_clock::now() < deadline); std::this_thread::yield();
    }
}
void setup_tests() {
    f.reset(); ia::Options disabled; ia::Sdk none; ia::start(sw, disabled, none, hardware);
    assert(!ia::status().running && f.creates == 0); error([] { ia::create(sw, attrs(1)); }, SAI_STATUS_NOT_SUPPORTED);
    auto o = options(); o.allow_unpoliced_cpu = false; error([&] { start(o); }); assert(f.creates == 0);
    error([&] { ia::start(sw, options(), none, hardware); }, SAI_STATUS_NOT_SUPPORTED);
    f.nodes.at(sw).attrs[SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY].ptr = nullptr; error([] { start(); }); assert(f.creates == 0);
    f.reset(); f.enumeration = false; error([] { start(); }); assert(f.creates == 0);
    f.reset(); f.capability = false; error([] { start(); }); assert(f.creates == 0);
    f.reset(); f.hostif.send_hostif_packet = nullptr; error([] { start(); }); assert(f.creates == 0);
    for (auto type : {SAI_HOSTIF_TRAP_TYPE_ARP_REQUEST, SAI_HOSTIF_TRAP_TYPE_IPV6_NEIGHBOR_DISCOVERY}) {
        f.reset(); f.add(9000, SAI_OBJECT_TYPE_HOSTIF_TRAP); f.s32(9000, SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE, type);
        error([] { start(); }, SAI_STATUS_ITEM_ALREADY_EXISTS); assert(f.nodes.count(9000) && f.creates == 0 && f.removes == 0);
    }
    for (unsigned step = 1; step <= 5; ++step) {
        f.reset(); f.fail_create = step; error([] { start(); });
        assert(!ia::status().running && !ia::status().trap_group && f.owned() == 0); ia::stop();
    }
    f.reset(); f.fail_get = 10001; error([] { start(); }); assert(f.owned() == 0); // Readback failure rolls back.
    f.reset(); f.fail_create = 5; f.fail_remove = 10002;
    error([] { start(); }); auto state = ia::status();
    assert(!state.running && state.tables[0] == 10002 && state.traps[0] == 10001 && state.trap_group == 10000 && !state.traps[1]);
    error([] { start(); }, SAI_STATUS_OBJECT_IN_USE); error([] { ia::stop(); });
    f.fail_remove = 0; ia::stop(); assert(f.owned() == 0 && !ia::status().trap_group);
    // Borrowed policer survives stop; no existing state is changed.
    f.reset(); f.add(8000, SAI_OBJECT_TYPE_POLICER); o = options(); o.policer = 8000; o.allow_unpoliced_cpu = false;
    start(o); assert(f.owned() == 5); error([] { start(); });
    auto group = ia::status().trap_group; assert(f.nodes.at(group).attrs.at(SAI_HOSTIF_TRAP_GROUP_ATTR_POLICER).oid == 8000);
    ia::stop(); assert(f.nodes.count(8000) && f.owned() == 0);
    for (unsigned index = 0; index < 5; ++index) {
        f.reset(); start(); f.fail_remove = 10000 + index; error([] { ia::stop(); });
        assert(!ia::status().running && f.nodes.count(f.fail_remove)); f.fail_remove = 0; ia::stop(); assert(f.owned() == 0);
    }
}
void address_tests() {
    f.reset(); f.access(1); f.access(2); start();
    auto a = ia::create(sw, attrs(1)); assert(a.key == "0x3e9@192.0.2.1/24" && a.attributes.at("address") == "192.0.2.1/24");
    assert(a.attributes.at("observation_source") == "software-responder");
    assert(ia::get(sw, "1001@192.0.2.1/24").key == a.key); error([] { ia::create(sw, attrs(1)); }, SAI_STATUS_ITEM_ALREADY_EXISTS);
    error([] { ia::create(sw, attrs(1, "192.0.2.1/32")); });
    auto b = ia::create(sw, attrs(2)); assert(a.key != b.key); // Same IP isolated in distinct VLANs is permitted.
    assert(ia::list(sw).size() == 2);
    auto v6 = ia::create(sw, attrs(1, "2001:0db8:0:0::1234/64"));
    assert(v6.key == "0x3e9@2001:db8::1234/64" && v6.attributes.at("dad") == "static-no-dad");
    for (const char* ip : {"192.0.2.1", "192.0.2.1/33", "2001:db8::1/129", "192.0.2.1/-1", "::/0", "::1/128", "ff02::1/64", "::ffff:192.0.2.1/128", "0.0.0.0/24", "127.0.0.1/8", "224.0.0.1/24", "192.0.2.1/24/junk"})
        error([&] { ia::create(sw, attrs(1, ip)); });
    auto wrong = attrs(1); wrong["extra"] = "x"; error([&] { ia::create(sw, wrong); });
    wrong = attrs(1, "192.0.2.3/24"); wrong["ingress_port"] = "202"; error([&] { ia::create(sw, wrong); });
    error([&] { ia::get(sw + 1, a.key); }); error([] { ia::get(sw, "bad"); });
    // Getter errors are not invented hardware observations; stale addresses remain removable.
    { std::lock_guard<std::mutex> l(hardware); f.u16(201, SAI_PORT_ATTR_PORT_VLAN_ID, 102); }
    error([&] { ia::get(sw, a.key); }); ia::remove(sw, a.key); error([&] { ia::get(sw, a.key); }, SAI_STATUS_ITEM_NOT_FOUND);
    ia::remove(sw, v6.key); ia::remove(sw, b.key); assert(ia::list(sw).empty());
    ia::stop(); f.reset(); f.access(1); auto o = options(); o.static_ipv6_no_dad = false; start(o);
    error([] { ia::create(sw, attrs(1, "2001:db8::1/64")); }, SAI_STATUS_NOT_SUPPORTED); ia::stop();
    // Each unsupported/ambiguous topology rejects address activation.
    for (unsigned test = 0; test < 10; ++test) {
        f.reset(); f.access(1);
        switch (test) {
        case 0: f.u16(201, SAI_PORT_ATTR_PORT_VLAN_ID, 102); break;
        case 1: f.s32(3001, SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE, SAI_VLAN_TAGGING_MODE_TAGGED); break;
        case 2: f.oid(4001, SAI_BRIDGE_PORT_ATTR_PORT_ID, 202); break;
        case 3: f.s32(1001, SAI_ROUTER_INTERFACE_ATTR_TYPE, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT); break;
        case 4: f.nodes.at(1001).attrs[SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS].mac[0] = 1; break;
        case 5: f.nodes.erase(3001); break;
        case 6: f.nodes.emplace(3999, f.nodes.at(3001)); break;
        case 7: f.flag(1001, SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE, false); break;
        case 8: f.s32(5000, SAI_BRIDGE_ATTR_TYPE, SAI_BRIDGE_TYPE_1D); break;
        case 9: f.fail_get = 1001; break;
        }
        start(); error([] { ia::create(sw, attrs(1)); }); assert(ia::status().addresses == 0); ia::stop();
    }
}
void worker_tests() {
    f.reset(); f.access(1); f.access(2); start();
    auto a = ia::create(sw, attrs(1)); ia::create(sw, attrs(2, "198.51.100.1/24"));
    ia::create(sw, attrs(1, "2001:db8:101::1/64"));
    auto state = ia::status(); auto p = arp(target("192.0.2.1")); inject_reliably(p, 201, state.traps[0]); wait_sent(1);
    assert(f.sent[0].first == 201 && be16(f.sent[0].second, 20) == 2);
    inject_reliably(ns(target("2001:db8:101::1")), 201, state.traps[1]); wait_sent(2); assert(f.sent[1].second[58] == 0xe0);
    inject_reliably(ns(target("2001:db8:101::1"), true, false), 201, state.traps[1]); wait_sent(3); assert(f.sent[2].second[58] == 0xa0);
    auto rejected = ia::status().rejected;
    for (auto port : {sai_object_id_t(202), sai_object_id_t(999)}) inject_reliably(p, port, state.traps[0]);
    inject_reliably(p, 201, state.traps[1]); inject_reliably(p, 201, 99999);
    auto tagged = p; put16(tagged, 12, 0x8100); inject_reliably(tagged, 201, state.traps[0]);
    wait_stat([&](const ia::Status& s) { return s.rejected >= rejected + 5; }); assert(f.sent.size() == 3);
    auto drops = ia::status().dropped; inject(p, 201, state.traps[0], sw + 1); inject(p, 201, state.traps[0], sw, true);
    inject(p, 0, state.traps[0]); assert(ia::status().dropped >= drops + 3);
    sai_attribute_t duplicate[3]{}; duplicate[0].id = duplicate[1].id = SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT;
    duplicate[0].value.oid = duplicate[1].value.oid = 201; duplicate[2].id = SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID; duplicate[2].value.oid = state.traps[0];
    ia::packet_callback()(sw, p.size(), p.data(), 3, duplicate); assert(ia::status().dropped >= drops + 4);
    // Stale PVID and stale MAC cannot elicit replies, and errors are observable.
    auto errors = ia::status().errors;
    { std::lock_guard<std::mutex> l(hardware); f.u16(201, SAI_PORT_ATTR_PORT_VLAN_ID, 102); }
    inject_reliably(p, 201, state.traps[0]); wait_stat([&](const ia::Status& s) { return s.errors > errors; }); assert(f.sent.size() == 3);
    { std::lock_guard<std::mutex> l(hardware); f.u16(201, SAI_PORT_ATTR_PORT_VLAN_ID, 101); f.nodes.at(1001).attrs[SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS].mac[5] = 2; }
    errors = ia::status().errors; inject_reliably(p, 201, state.traps[0]); wait_stat([&](const ia::Status& s) { return s.errors > errors; }); assert(f.sent.size() == 3);
    ia::remove(sw, a.key); ia::stop();
    inject(p, 201, state.traps[0]); assert(!ia::status().running && f.owned() == 0);
    // All 32 access VLANs (101..132), both families, plus a direct 10G port RIF.
    f.reset(); for (unsigned n = 1; n <= 33; ++n) f.access(n);
    f.s32(1033, SAI_ROUTER_INTERFACE_ATTR_TYPE, SAI_ROUTER_INTERFACE_TYPE_PORT); f.oid(1033, SAI_ROUTER_INTERFACE_ATTR_PORT_ID, 233);
    start();
    for (unsigned n = 1; n <= 33; ++n) {
        ia::create(sw, attrs(n, "10.0." + std::to_string(n) + ".1/24"));
        ia::create(sw, attrs(n, "2001:db8:" + std::to_string(n) + "::1/64"));
    }
    assert(ia::status().addresses == 66);
    state = ia::status();
    for (unsigned n = 1; n <= 33; ++n) {
        inject_reliably(arp(target(("10.0." + std::to_string(n) + ".1").c_str())), 200 + n, state.traps[0]); wait_sent(2*n - 1);
        inject_reliably(ns(target(("2001:db8:" + std::to_string(n) + "::1").c_str())), 200 + n, state.traps[1]); wait_sent(2*n);
    }
    ia::stop(); assert(f.owned() == 0);
    // Explicit send failure is retained in observable diagnostics, not counted as success.
    f.reset(); f.access(1); start(); ia::create(sw, attrs(1)); state = ia::status(); f.send_error = true;
    inject_reliably(p, 201, state.traps[0]); wait_stat([&](const ia::Status& s) { return s.errors > state.errors; });
    assert(f.sent.empty() && ia::status().last_status == SAI_STATUS_NOT_SUPPORTED && !ia::status().running);
    error([] { ia::create(sw, attrs(1, "192.0.2.3/24")); }, SAI_STATUS_NOT_SUPPORTED);
    error([] { ia::get(sw, "1001@192.0.2.1/24"); }, SAI_STATUS_NOT_SUPPORTED);
    error([] { ia::list(sw); }, SAI_STATUS_NOT_SUPPORTED);
    // A fault must not strand addresses: removal still clears them so that
    // topology mutations are no longer blocked.
    ia::remove(sw, "1001@192.0.2.1/24"); assert(ia::status().addresses == 0);
    error([] { ia::remove(sw, "1001@192.0.2.1/24"); }, SAI_STATUS_ITEM_NOT_FOUND); ia::stop();
}
void bounded_queue_tests() {
    f.reset(); f.access(1); start(); ia::create(sw, attrs(1)); auto before = ia::status();
    auto p = arp(target("192.0.2.1"));
    { std::lock_guard<std::mutex> l(f.sent_mutex); f.hold_send = true; }
    inject(p, 201, before.traps[0]);
    {
        std::unique_lock<std::mutex> l(f.sent_mutex);
        assert(f.sent_cv.wait_for(l, std::chrono::seconds(3), [] { return f.entered_send; }));
    }
    // Worker is inside SAI while callback is still bounded and does not call SDK.
    for (unsigned i = 0; i < 1000; ++i) inject(p, 201, before.traps[0]);
    { std::lock_guard<std::mutex> l(f.sent_mutex); f.hold_send = false; } f.sent_cv.notify_all();
    auto after = ia::status(); assert(after.admitted - before.admitted <= 65 && after.dropped - before.dropped >= 936);
    wait_stat([&](const ia::Status& s) { return s.queued == 0; });
    // Admission remains bounded to 100 in this fixed one-second window, independent of queue drain.
    for (unsigned i = 0; i < 1000; ++i) inject(p, 201, before.traps[0]);
    after = ia::status(); assert(after.admitted - before.admitted <= 100);
    ia::stop(); auto sent = f.sent.size();
    for (unsigned i = 0; i < 1000; ++i) inject(p, 201, before.traps[0]);
    assert(f.sent.size() == sent && ia::status().queued == 0);
    // Concurrent SDK callback producers may outlive stop, but cannot access
    // removed SDK objects or send after worker join. No callback retains a buffer.
    f.reset(); f.access(1); start(); ia::create(sw, attrs(1)); before = ia::status();
    std::atomic<bool> go{false};
    auto flood = [&] {
        while (!go.load()) std::this_thread::yield();
        for (unsigned i = 0; i < 10000; ++i) inject(p, 201, before.traps[0]);
    };
    std::thread first(flood), second(flood); go = true;
    ia::stop(); sent = f.sent.size(); first.join(); second.join();
    assert(f.sent.size() == sent && f.owned() == 0 && ia::status().queued == 0);
}
} // namespace
int main() {
    packet_tests(); setup_tests(); address_tests(); worker_tests(); bounded_queue_tests(); ia::stop();
    std::cout << "interface_address: pure packet + fake SAI lifecycle/ownership/topology/worker/bounds tests passed\n";
    return 0;
}
