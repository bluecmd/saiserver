// Fake SAI SDK and packet builders shared by the interface_address tests.
#include "tests/server/fake_sdk.h"

#include <arpa/inet.h>
#include <algorithm>
#include <cassert>
#include <chrono>
#include <cstring>
#include <thread>

namespace fake_sdk {
std::mutex hardware;
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
Bytes ns(const ia::Target& t, bool dad, bool slla) {
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
Fake f;
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
void start(const ia::Options& o) { ia::start(sw, o, sdk(), hardware); }
ia::Attributes attrs(unsigned n, const std::string& ip) {
    return {{"router_interface", std::to_string(1000 + n)}, {"ingress_port", std::to_string(200 + n)}, {"address", ip}};
}
void error(const std::function<void()>& call, sai_status_t expected) {
    bool caught = false;
    try { call(); } catch (const ia::Error& e) { caught = true; if (expected != SAI_STATUS_SUCCESS) assert(e.status == expected); }
    assert(caught);
}
void inject(const Bytes& p, sai_object_id_t port, sai_object_id_t trap, sai_object_id_t switch_oid, bool lag) {
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
}  // namespace fake_sdk
