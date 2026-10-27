#include "tui_rpc.h"
#include "switch_sai_rpc.h"
extern "C" {
#include <sai.h>
}
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/transport/TBufferTransports.h>
#include <arpa/inet.h>
#include <cassert>
#include <cstring>
#include <functional>
#include <iostream>
#include <set>
#include <sstream>

namespace {
using Attrs = std::map<std::string, std::string>;
struct Record {
    std::string kind;
    std::map<sai_attr_id_t, sai_attribute_value_t> values;
    std::map<sai_attr_id_t, std::vector<sai_object_id_t>> lists;
};
std::map<sai_object_id_t, Record> records;
std::map<std::string, Record> entries;
uint64_t nextid = 100;
unsigned queries = 0, mutations = 0, gets = 0, writes = 0;
sai_attr_id_t failget = UINT32_MAX;
unsigned failwrite = 0;
bool failcreate = false, wrongread = false, keepremoved = false;
std::set<sai_stat_id_t> unsupported_stats;
sai_stat_id_t broken_stat = UINT32_MAX;
sai_status_t query_status = SAI_STATUS_SUCCESS;
sai_status_t forced_get_status = SAI_STATUS_SUCCESS;
std::string h(uint64_t id) { std::ostringstream s; s << "0x" << std::hex << id; return s.str(); }
std::string nk(const sai_neighbor_entry_t* e) {
    char s[INET6_ADDRSTRLEN]; bool v4 = e->ip_address.addr_family == SAI_IP_ADDR_FAMILY_IPV4;
    inet_ntop(v4 ? AF_INET : AF_INET6, &e->ip_address.addr, s, sizeof(s));
    return h(e->rif_id) + "@" + s;
}
std::string rk(const sai_route_entry_t* e) {
    char s[INET6_ADDRSTRLEN]; bool v4 = e->destination.addr_family == SAI_IP_ADDR_FAMILY_IPV4;
    inet_ntop(v4 ? AF_INET : AF_INET6, &e->destination.addr, s, sizeof(s));
    const auto* m = reinterpret_cast<const uint8_t*>(&e->destination.mask);
    unsigned n = 0; for (unsigned i = 0; i < (v4 ? 4u : 16u); ++i) n += __builtin_popcount(m[i]);
    return h(e->vr_id) + "@" + s + "/" + std::to_string(n);
}
void store(Record& r, uint32_t n, const sai_attribute_t* a) {
    for (unsigned i = 0; i < n; ++i) {
        if (r.kind == "acl_table" && a[i].id == SAI_ACL_TABLE_ATTR_ACL_BIND_POINT_TYPE_LIST) {
            assert(a[i].value.s32list.count == 1 && a[i].value.s32list.list[0] == SAI_ACL_BIND_POINT_TYPE_PORT); continue;
        }
        if (r.kind == "acl_table" && a[i].id == SAI_ACL_TABLE_ATTR_ACL_ACTION_TYPE_LIST) {
            assert(a[i].value.s32list.count == 1 && a[i].value.s32list.list[0] == SAI_ACL_ACTION_TYPE_PACKET_ACTION); continue;
        }
        if (r.kind == "acl_group" && a[i].id == SAI_ACL_TABLE_GROUP_ATTR_ACL_BIND_POINT_TYPE_LIST) {
            assert(a[i].value.s32list.count == 1 && a[i].value.s32list.list[0] == SAI_ACL_BIND_POINT_TYPE_PORT); continue;
        }
        r.values[a[i].id] = a[i].value;
    }
}
sai_status_t create(const char* kind, sai_object_id_t* id, uint32_t n, const sai_attribute_t* a) {
    ++mutations; if (failcreate) return SAI_STATUS_TABLE_FULL;
    *id = nextid++; records[*id].kind = kind; store(records[*id], n, a); return SAI_STATUS_SUCCESS;
}
sai_status_t read(Record& r, uint32_t n, sai_attribute_t* a) {
    ++gets; assert(n == 1);
    if (a->id == failget) return SAI_STATUS_NOT_SUPPORTED;
    if (r.lists.count(a->id)) {
        auto& v = r.lists.at(a->id); auto cap = a->value.objlist.count; a->value.objlist.count = v.size();
        if (cap < v.size()) return SAI_STATUS_BUFFER_OVERFLOW;
        if (!v.empty()) std::memcpy(a->value.objlist.list, v.data(), v.size() * sizeof(sai_object_id_t));
        return SAI_STATUS_SUCCESS;
    }
    // SAI defaults in the fake ASIC, not the adapter under test.
    if (r.kind == "vlan" && a->id == SAI_VLAN_ATTR_MEMBER_LIST) { a->value.objlist.count = 0; return SAI_STATUS_SUCCESS; }
    if (r.kind == "port" && a->id == SAI_PORT_ATTR_HW_LANE_LIST) {
        auto cap = a->value.u32list.count; a->value.u32list.count = 2;
        if (cap < 2) return SAI_STATUS_BUFFER_OVERFLOW;
        a->value.u32list.list[0] = 11; a->value.u32list.list[1] = 12; return SAI_STATUS_SUCCESS;
    }
    a->value = r.values[a->id];
    if (wrongread && r.kind == "vlan" && a->id == SAI_VLAN_ATTR_VLAN_ID) ++a->value.u16;
    return SAI_STATUS_SUCCESS;
}
sai_status_t getoid(sai_object_id_t id, uint32_t n, sai_attribute_t* a) {
    if (forced_get_status != SAI_STATUS_SUCCESS) return forced_get_status;
    if (!records.count(id)) return SAI_STATUS_ITEM_NOT_FOUND;
    return read(records.at(id), n, a);
}
sai_status_t setoid(sai_object_id_t id, const sai_attribute_t* a) {
    ++mutations; ++writes;
    if (writes == failwrite) return SAI_STATUS_OBJECT_IN_USE;
    if (!records.count(id)) return SAI_STATUS_ITEM_NOT_FOUND;
    records[id].values[a->id] = a->value; return SAI_STATUS_SUCCESS;
}
sai_status_t removeoid(sai_object_id_t id) {
    ++mutations; if (!records.count(id)) return SAI_STATUS_ITEM_NOT_FOUND;
    if (!keepremoved) records.erase(id);
    return SAI_STATUS_SUCCESS;
}
#define CREATOR(NAME) sai_status_t create_##NAME(sai_object_id_t* id, sai_object_id_t sw, uint32_t n, const sai_attribute_t* a) { assert(sw == 1); return create(#NAME, id, n, a); }
CREATOR(port) CREATOR(vlan) CREATOR(vlan_member) CREATOR(bridge_port) CREATOR(virtual_router)
CREATOR(router_interface) CREATOR(next_hop) CREATOR(acl_table) CREATOR(acl_entry) CREATOR(acl_group) CREATOR(acl_group_member)
#undef CREATOR
sai_status_t cn(const sai_neighbor_entry_t* e, uint32_t n, const sai_attribute_t* a) {
    ++mutations; assert(e->switch_id == 1); auto k = nk(e);
    if (entries.count(k)) return SAI_STATUS_ITEM_ALREADY_EXISTS;
    entries[k].kind = "neighbor"; store(entries[k], n, a); return SAI_STATUS_SUCCESS;
}
sai_status_t cr(const sai_route_entry_t* e, uint32_t n, const sai_attribute_t* a) {
    ++mutations; assert(e->switch_id == 1); auto k = rk(e);
    if (entries.count(k)) return SAI_STATUS_ITEM_ALREADY_EXISTS;
    entries[k].kind = "route"; store(entries[k], n, a); return SAI_STATUS_SUCCESS;
}
sai_status_t gn(const sai_neighbor_entry_t* e, uint32_t n, sai_attribute_t* a) { return entries.count(nk(e)) ? read(entries.at(nk(e)), n, a) : SAI_STATUS_ITEM_NOT_FOUND; }
sai_status_t gr(const sai_route_entry_t* e, uint32_t n, sai_attribute_t* a) { return entries.count(rk(e)) ? read(entries.at(rk(e)), n, a) : SAI_STATUS_ITEM_NOT_FOUND; }
sai_status_t sn(const sai_neighbor_entry_t* e, const sai_attribute_t* a) { ++mutations; if (!entries.count(nk(e))) return SAI_STATUS_ITEM_NOT_FOUND; store(entries.at(nk(e)), 1, a); return SAI_STATUS_SUCCESS; }
sai_status_t sr(const sai_route_entry_t* e, const sai_attribute_t* a) { ++mutations; if (!entries.count(rk(e))) return SAI_STATUS_ITEM_NOT_FOUND; store(entries.at(rk(e)), 1, a); return SAI_STATUS_SUCCESS; }
sai_status_t rn(const sai_neighbor_entry_t* e) { ++mutations; return entries.erase(nk(e)) ? SAI_STATUS_SUCCESS : SAI_STATUS_ITEM_NOT_FOUND; }
sai_status_t rr(const sai_route_entry_t* e) { ++mutations; return entries.erase(rk(e)) ? SAI_STATUS_SUCCESS : SAI_STATUS_ITEM_NOT_FOUND; }
sai_status_t gf(const sai_fdb_entry_t* e, uint32_t n, sai_attribute_t* a) {
    assert(e->switch_id == 1 && e->bv_id == 2 && e->mac_address[0] == 0xaa);
    Record r; if (a->id == SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID) r.values[a->id].oid = 7;
    if (a->id == SAI_FDB_ENTRY_ATTR_TYPE) r.values[a->id].s32 = SAI_FDB_ENTRY_TYPE_DYNAMIC;
    return read(r, n, a);
}
sai_status_t stats(sai_object_id_t id, uint32_t n, const sai_stat_id_t* stat, uint64_t* out) {
    assert(n == 1); if (id != 5) return SAI_STATUS_INVALID_OBJECT_ID;
    if (*stat == broken_stat) return SAI_STATUS_FAILURE;
    if (unsupported_stats.count(*stat)) return SAI_STATUS_NOT_SUPPORTED;
    *out = *stat == SAI_PORT_STAT_IF_IN_OCTETS ? UINT64_MAX : 3; return SAI_STATUS_SUCCESS;
}
sai_port_api_t ports{}; sai_vlan_api_t vlans{}; sai_bridge_api_t bridges{};
sai_virtual_router_api_t vrs{}; sai_router_interface_api_t rifs{}; sai_next_hop_api_t nhs{};
sai_neighbor_api_t neighbors{}; sai_route_api_t routes{}; sai_acl_api_t acls{};
sai_switch_api_t switches{}; sai_fdb_api_t fdb{};
void init() {
#define BIND(TABLE, NAME, CREATE) TABLE.create_##NAME = CREATE; TABLE.remove_##NAME = removeoid; TABLE.set_##NAME##_attribute = setoid; TABLE.get_##NAME##_attribute = getoid
    BIND(ports, port, create_port); BIND(vlans, vlan, create_vlan); BIND(vlans, vlan_member, create_vlan_member);
    BIND(bridges, bridge_port, create_bridge_port); bridges.get_bridge_attribute = getoid;
    BIND(vrs, virtual_router, create_virtual_router); BIND(rifs, router_interface, create_router_interface);
    BIND(nhs, next_hop, create_next_hop); BIND(acls, acl_table, create_acl_table); BIND(acls, acl_entry, create_acl_entry);
    BIND(acls, acl_table_group, create_acl_group); BIND(acls, acl_table_group_member, create_acl_group_member);
#undef BIND
    switches.get_switch_attribute = getoid; ports.get_port_stats = stats;
    neighbors.create_neighbor_entry = cn; neighbors.get_neighbor_entry_attribute = gn; neighbors.set_neighbor_entry_attribute = sn; neighbors.remove_neighbor_entry = rn;
    routes.create_route_entry = cr; routes.get_route_entry_attribute = gr; routes.set_route_entry_attribute = sr; routes.remove_route_entry = rr;
    fdb.get_fdb_entry_attribute = gf;
    auto& sw = records[1]; sw.kind = "switch";
    sw.values[SAI_SWITCH_ATTR_DEFAULT_VLAN_ID].oid = 2;
    sw.values[SAI_SWITCH_ATTR_DEFAULT_VIRTUAL_ROUTER_ID].oid = 3;
    sw.values[SAI_SWITCH_ATTR_DEFAULT_1Q_BRIDGE_ID].oid = 4;
    sw.lists[SAI_SWITCH_ATTR_PORT_LIST] = {5};
    records[2].kind = "vlan"; records[2].values[SAI_VLAN_ATTR_VLAN_ID].u16 = 1; records[2].lists[SAI_VLAN_ATTR_MEMBER_LIST] = {6};
    records[3].kind = "virtual_router";
    records[4].kind = "bridge"; records[4].lists[SAI_BRIDGE_ATTR_PORT_LIST] = {7, 8};
    records[5].kind = "port";
    records[6].kind = "vlan_member"; records[6].values[SAI_VLAN_MEMBER_ATTR_VLAN_ID].oid = 2; records[6].values[SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID].oid = 7;
    records[7].kind = "bridge_port"; records[7].values[SAI_BRIDGE_PORT_ATTR_TYPE].s32 = SAI_BRIDGE_PORT_TYPE_PORT; records[7].values[SAI_BRIDGE_PORT_ATTR_PORT_ID].oid = 5;
    records[8].kind = "bridge_port"; records[8].values[SAI_BRIDGE_PORT_ATTR_TYPE].s32 = SAI_BRIDGE_PORT_TYPE_1D_ROUTER; records[8].values[SAI_BRIDGE_PORT_ATTR_RIF_ID].oid = 9;
    records[9].kind = "router_interface"; records[9].values[SAI_ROUTER_INTERFACE_ATTR_TYPE].s32 = SAI_ROUTER_INTERFACE_TYPE_BRIDGE;
}
void error(const std::function<void()>& f, sai_status_t status, const std::string& message = "") {
    try { f(); assert(!"expected RpcError"); }
    catch (const sai_tui::RpcError& e) { assert(e.status == status); if (e.message.find(message) == std::string::npos) { std::cerr << e.message << " missing: " << message << '\n'; assert(false); } }
}
void validation() {
    sai_tui::Object o;
    auto badcreate = [&](const std::string& kind, const Attrs& a) {
        auto before = queries;
        error([&] { tui_rpc::create(o, 1, kind, a); }, SAI_STATUS_INVALID_PARAMETER);
        assert(queries == before);
    };
    badcreate("nonsense", {});
    for (const char* kind : {"vlan", "vlan_member", "bridge_port", "virtual_router", "router_interface", "next_hop", "neighbor", "route", "acl_table", "acl_entry", "acl_group", "acl_group_member"})
        badcreate(kind, {{"unknown", "not-ignored"}});
    for (const char* n : {"0", "4095", "65536", "-1", "+1", " 2", "2 ", "1x", "18446744073709551616"}) badcreate("vlan", {{"vlan_id", n}});
    badcreate("vlan", {{"vlan_id", "3"}, {"ignored", "x"}});
    badcreate("virtual_router", {{"ipv4", "1"}});
    badcreate("router_interface", {{"virtual_router", "3"}, {"port", "5"}, {"vlan", "2"}});
    badcreate("router_interface", {{"virtual_router", "3"}});
    badcreate("next_hop", {{"router_interface", "0xg"}, {"ip", "1.1.1.1"}});
    badcreate("next_hop", {{"router_interface", "9"}, {"ip", std::string("1.1.1.1\0suffix", 14)}});
    badcreate("neighbor", {{"router_interface", "9"}, {"ip", "::g"}, {"mac", "aa:bb:cc:dd:ee:ff"}});
    badcreate("neighbor", {{"router_interface", "9"}, {"ip", "::1"}, {"mac", "aa:bb:cc:dd:ee:f"}});
    badcreate("route", {{"virtual_router", "3"}, {"prefix", "::1/129"}, {"next_hop", "10"}});
    badcreate("route", {{"virtual_router", "3"}, {"prefix", "1.1.1.1/-1"}, {"next_hop", "10"}});
    badcreate("acl_table", {{"stage", "egress"}, {"family", "mixed"}});
    badcreate("acl_entry", {{"table", "10"}, {"action", "deny"}, {"priority", "4294967296"}});
    badcreate("acl_entry", {{"table", "10"}, {"action", "deny"}, {"priority", "1"}, {"protocol", "256"}});
    for (const char* kind : {"port", "vlan", "next_hop", "neighbor", "route"}) {
        auto before = queries;
        error([&] { tui_rpc::get(o, 1, kind, " -1"); }, SAI_STATUS_INVALID_PARAMETER); assert(queries == before);
    }
    auto before = queries;
    error([&] { tui_rpc::set(o, 1, "next_hop", "0x10", {{"ip", "::1"}}); }, SAI_STATUS_INVALID_PARAMETER, "immutable");
    error([&] { tui_rpc::set(o, 1, "port", "5", {{"admin", "true"}, {"unknown", "1"}}); }, SAI_STATUS_INVALID_PARAMETER);
    error([&] { tui_rpc::set(o, 1, "port", "5", {{"speed", "10000"}}); }, SAI_STATUS_INVALID_PARAMETER);
    error([&] { tui_rpc::set(o, 1, "port", "5", {}); }, SAI_STATUS_INVALID_PARAMETER);
    error([&] { tui_rpc::remove(1, "port", "5"); }, SAI_STATUS_NOT_SUPPORTED);
    error([&] { tui_rpc::create(o, 1, "fdb", {}); }, SAI_STATUS_NOT_SUPPORTED);
    assert(queries == before);
}
sai_tui::Object make(const std::string& kind, const Attrs& a) {
    sai_tui::Object o; auto old = gets; tui_rpc::create(o, 1, kind, a); assert(gets > old); assert(o.kind == kind); return o;
}
void crud() {
    sai_tui::Object o;
    wrongread = true; auto vlan = make("vlan", {{"vlan_id", "123"}}); assert(vlan.attributes.at("vlan_id") == "124"); wrongread = false;
    auto bp = make("bridge_port", {{"port", "5"}, {"bridge", "4"}}); assert(bp.attributes.at("admin") == "true"); assert(bp.attributes.at("bridge") == "0x4");
    tui_rpc::set(o, 1, "bridge_port", bp.key, {{"admin", "false"}, {"learning", "disable"}});
    assert(o.attributes.at("admin") == "false" && o.attributes.at("learning") == "disable");
    auto before = mutations;
    error([&] { tui_rpc::create(o, 1, "bridge_port", {{"port", "5"}, {"bridge", "99"}}); }, SAI_STATUS_NOT_SUPPORTED); assert(mutations == before);
    auto vm = make("vlan_member", {{"vlan", vlan.key}, {"bridge_port", bp.key}, {"tagging", "tagged"}});
    tui_rpc::set(o, 1, "vlan_member", vm.key, {{"tagging", "untagged"}}); assert(o.attributes.at("tagging") == "untagged");
    auto vr = make("virtual_router", {}); assert(vr.attributes.at("ipv4") == "true" && vr.attributes.at("ipv6") == "true");
    tui_rpc::set(o, 1, "virtual_router", vr.key, {{"ipv4", "false"}}); assert(o.attributes.at("ipv4") == "false");
    auto rif = make("router_interface", {{"virtual_router", vr.key}, {"port", "5"}, {"mtu", "9000"}, {"src_mac", "aa:bb:cc:dd:ee:ff"}});
    assert(rif.attributes.count("port") && !rif.attributes.count("vlan"));
    auto rv = make("router_interface", {{"virtual_router", vr.key}, {"vlan", vlan.key}}); assert(rv.attributes.count("vlan") && !rv.attributes.count("port"));
    tui_rpc::set(o, 1, "router_interface", rif.key, {{"mtu", "1500"}, {"ipv6", "false"}}); assert(o.attributes.at("mtu") == "1500");
    auto nh = make("next_hop", {{"router_interface", rif.key}, {"ip", "2001:db8::1"}}); assert(nh.attributes.at("ip") == "2001:db8::1");
    auto nh4 = make("next_hop", {{"router_interface", rif.key}, {"ip", "192.0.2.1"}});
    for (const char* address : {"192.0.2.1", "2001:0db8::1"}) {
        auto n = make("neighbor", {{"router_interface", rif.key}, {"ip", address}, {"mac", "aa:bb:cc:dd:ee:ff"}});
        tui_rpc::set(o, 1, "neighbor", n.key, {{"mac", "00:01:02:03:04:05"}}); assert(o.attributes.at("mac") == "00:01:02:03:04:05");
        tui_rpc::remove(1, "neighbor", n.key);
    }
    for (const char* cidr : {"192.0.2.99/24", "2001:db8::999/64", "::1/0", "192.0.2.1/32"}) {
        auto r = make("route", {{"virtual_router", vr.key}, {"prefix", cidr}, {"next_hop", nh.key}});
        if (std::string(cidr) == "192.0.2.99/24") assert(r.attributes.at("prefix") == "192.0.2.0/24");
        if (std::string(cidr) == "2001:db8::999/64") assert(r.attributes.at("prefix") == "2001:db8::/64");
        if (std::string(cidr) == "::1/0") assert(r.attributes.at("prefix") == "::/0");
        tui_rpc::set(o, 1, "route", r.key, {{"next_hop", "0"}, {"action", "drop"}}); assert(o.attributes.at("action") == "drop");
        tui_rpc::remove(1, "route", r.key);
    }
    for (const char* family : {"ipv4", "ipv6"}) {
        bool v4 = std::string(family) == "ipv4";
        auto t = make("acl_table", {{"family", family}, {"stage", "ingress"}}); assert(t.attributes.at("family") == family);
        auto g = make("acl_group", {{"stage", "ingress"}});
        auto m = make("acl_group_member", {{"table", t.key}, {"group", g.key}, {"priority", "123"}});
        error([&] { tui_rpc::set(o, 1, "acl_group_member", m.key, {{"priority", "456"}}); }, SAI_STATUS_INVALID_PARAMETER, "immutable");
        tui_rpc::set(o, 1, "port", "5", {{"ingress_acl", g.key}, {"egress_acl", "0"}, {"pvid", "123"}, {"admin", "true"}});
        assert(o.attributes.at("ingress_acl") == g.key && o.attributes.at("lanes") == "11,12");
        auto e = make("acl_entry", {{"table", t.key}, {"priority", "500"}, {"action", "deny"}, {"src", v4 ? "192.0.2.17/24" : "2001:db8::17/64"}, {"protocol", "6"}});
        assert(e.attributes.at("src") == (v4 ? "192.0.2.0/24" : "2001:db8::/64")); assert(!e.attributes.count("dst")); assert(e.attributes.at("protocol") == "6");
        auto before = mutations;
        error([&] { tui_rpc::set(o, 1, "acl_entry", e.key, {{"src", v4 ? "::/0" : "0.0.0.0/0"}}); }, SAI_STATUS_INVALID_PARAMETER); assert(mutations == before);
        tui_rpc::set(o, 1, "acl_entry", e.key, {{"enable", "false"}, {"priority", "100"}, {"action", "permit"}, {"dst", v4 ? "0.0.0.0/0" : "::/0"}, {"protocol", "17"}});
        assert(o.attributes.at("enable") == "false" && o.attributes.at("action") == "permit" && o.attributes.at("protocol") == "17");
        auto eid = std::stoull(e.key, nullptr, 16);
        auto protocolid = v4 ? SAI_ACL_ENTRY_ATTR_FIELD_IP_PROTOCOL : SAI_ACL_ENTRY_ATTR_FIELD_IPV6_NEXT_HEADER;
        records[eid].values[protocolid].aclfield.mask.u8 = 15;
        error([&] { tui_rpc::get(o, 1, "acl_entry", e.key); }, SAI_STATUS_NOT_SUPPORTED, "non-exact mask");
        records[eid].values[protocolid].aclfield.mask.u8 = 255;
        tui_rpc::set(o, 1, "port", "5", {{"ingress_acl", "0x0"}}); assert(o.attributes.at("ingress_acl") == "0x0");
        tui_rpc::remove(1, "acl_entry", e.key); tui_rpc::remove(1, "acl_group_member", m.key); tui_rpc::remove(1, "acl_group", g.key); tui_rpc::remove(1, "acl_table", t.key);
    }
    tui_rpc::get(o, 1, "fdb", "2@AA:BB:CC:DD:EE:FF"); assert(o.key == "0x2@aa:bb:cc:dd:ee:ff" && o.attributes.at("bridge_port") == "0x7");
    for (const auto& obj : {nh4, nh, rv, rif, vr, vm, bp, vlan}) tui_rpc::remove(1, obj.kind, obj.key);
}
void failures() {
    sai_tui::Object o;
    failcreate = true;
    error([&] { tui_rpc::create(o, 1, "vlan", {{"vlan_id", "9"}}); }, SAI_STATUS_TABLE_FULL);
    failcreate = false;
    failget = SAI_VLAN_ATTR_VLAN_ID; auto id = nextid;
    error([&] { tui_rpc::create(o, 1, "vlan", {{"vlan_id", "9"}}); }, SAI_STATUS_NOT_SUPPORTED, "READBACK FAILED");
    assert(records.count(id)); failget = UINT32_MAX;
    tui_rpc::get(o, 1, "vlan", h(id)); assert(o.attributes.at("vlan_id") == "9");
    sai_tui::Inventory inv; tui_rpc::snapshot(inv, 1); bool found = false;
    for (const auto& obj : inv.objects) if (obj.kind == "vlan" && obj.key == h(id)) found = true;
    assert(found); // Created key survives readback failure; values are re-read.
    keepremoved = true;
    error([&] { tui_rpc::remove(1, "vlan", h(id)); }, SAI_STATUS_FAILURE, "still readable");
    keepremoved = false;
    auto saved = records.at(id); forced_get_status = SAI_STATUS_FAILURE;
    error([&] { tui_rpc::remove(1, "vlan", h(id)); }, SAI_STATUS_FAILURE, "absence could not be confirmed");
    assert(!records.count(id)); forced_get_status = SAI_STATUS_SUCCESS;
    records[id] = saved; tui_rpc::remove(1, "vlan", h(id));
    auto before_query_failure = mutations;
    query_status = SAI_STATUS_UNINITIALIZED;
    error([&] { tui_rpc::set(o, 1, "port", "5", {{"admin", "true"}}); }, SAI_STATUS_UNINITIALIZED, "after 0 successful writes");
    assert(mutations == before_query_failure); query_status = SAI_STATUS_SUCCESS;
    failwrite = writes + 2;
    auto reads_before_partial = gets;
    error([&] { tui_rpc::set(o, 1, "port", "5", {{"admin", "false"}, {"pvid", "100"}}); }, SAI_STATUS_OBJECT_IN_USE, "partial readback observed");
    assert(gets > reads_before_partial);
    failwrite = writes + 2; failget = SAI_PORT_ATTR_SPEED;
    error([&] { tui_rpc::set(o, 1, "port", "5", {{"admin", "false"}, {"pvid", "100"}}); }, SAI_STATUS_OBJECT_IN_USE, "PARTIAL READBACK FAILED");
    failwrite = 0; failget = UINT32_MAX;
    tui_rpc::get(o, 1, "port", "5"); assert(o.attributes.at("admin") == "false");
    failget = SAI_PORT_ATTR_SPEED;
    error([&] { tui_rpc::set(o, 1, "port", "5", {{"admin", "true"}}); }, SAI_STATUS_NOT_SUPPORTED, "READBACK FAILED");
    failget = UINT32_MAX;
    // Objects on a table lacking protocol support must not silently ignore protocol.
    auto t = make("acl_table", {{"family", "ipv4"}, {"stage", "egress"}});
    auto tid = std::stoull(t.key, nullptr, 16); records[tid].values[SAI_ACL_TABLE_ATTR_FIELD_IP_PROTOCOL].booldata = false;
    auto before = mutations;
    error([&] { tui_rpc::create(o, 1, "acl_entry", {{"table", t.key}, {"priority", "1"}, {"action", "deny"}, {"protocol", "6"}}); }, SAI_STATUS_NOT_SUPPORTED, "does not support protocol"); assert(mutations == before);
    tui_rpc::remove(1, "acl_table", t.key);
}
void inventory_counters() {
    sai_tui::Inventory inv; tui_rpc::snapshot(inv, 1);
    assert(inv.objects.size() == 9 && inv.warnings.size() == 2);
    std::set<std::string> keys; for (const auto& o : inv.objects) keys.insert(o.kind + ":" + o.key);
    assert(keys.count("router_interface:0x9") && keys.count("port:0x5"));
    failget = SAI_PORT_ATTR_SPEED; tui_rpc::snapshot(inv, 1); assert(inv.warnings.size() == 3); failget = UINT32_MAX;
    failget = SAI_SWITCH_ATTR_SRC_MAC_ADDRESS; tui_rpc::snapshot(inv, 1);
    assert(inv.objects.size() == 8 && inv.warnings.size() == 3); failget = UINT32_MAX;
    std::map<std::string, int64_t> c; tui_rpc::port_counters(c, 1, "5");
    assert(c.size() == 8 && c.at("in_octets") == -1 && c.at("in_packets") == 9);
    unsupported_stats = {SAI_PORT_STAT_IF_OUT_ERRORS, SAI_PORT_STAT_IF_IN_MULTICAST_PKTS};
    tui_rpc::port_counters(c, 1, "5"); assert(c.size() == 6 && !c.count("out_errors") && !c.count("in_packets"));
    broken_stat = SAI_PORT_STAT_IF_OUT_OCTETS;
    error([&] { tui_rpc::port_counters(c, 1, "5"); }, SAI_STATUS_FAILURE);
    broken_stat = SAI_PORT_STAT_IF_IN_BROADCAST_PKTS;
    error([&] { tui_rpc::port_counters(c, 1, "5"); }, SAI_STATUS_FAILURE, "broadcast");
    broken_stat = UINT32_MAX;
    unsupported_stats = {SAI_PORT_STAT_IF_IN_OCTETS, SAI_PORT_STAT_IF_OUT_OCTETS,
        SAI_PORT_STAT_IF_IN_UCAST_PKTS, SAI_PORT_STAT_IF_OUT_UCAST_PKTS,
        SAI_PORT_STAT_IF_IN_ERRORS, SAI_PORT_STAT_IF_OUT_ERRORS,
        SAI_PORT_STAT_IF_IN_DISCARDS, SAI_PORT_STAT_IF_OUT_DISCARDS};
    error([&] { tui_rpc::port_counters(c, 1, "5"); }, SAI_STATUS_NOT_SUPPORTED, "all eight keys unavailable");
    unsupported_stats.clear();
    error([&] { tui_rpc::port_counters(c, 1, "99"); }, SAI_STATUS_INVALID_OBJECT_ID);
}
// Inherited processor fallback must carry the declared RpcError over binary Thrift.
struct WireHandler : switch_sai::switch_sai_rpcNull {
    void tui_get(sai_tui::Object& o, const std::string& k, const std::string& key) override { tui_rpc::get(o, 1, k, key); }
    void tui_create(sai_tui::Object& o, const std::string& k, const Attrs& a) override { tui_rpc::create(o, 1, k, a); }
};
void wire() {
    using apache::thrift::transport::TMemoryBuffer;
    using apache::thrift::protocol::TBinaryProtocol;
    auto req = std::make_shared<TMemoryBuffer>(); auto res = std::make_shared<TMemoryBuffer>();
    auto in = std::make_shared<TBinaryProtocol>(req); auto out = std::make_shared<TBinaryProtocol>(res);
    switch_sai::switch_sai_rpcClient client(out, in);
    switch_sai::switch_sai_rpcProcessor processor(std::make_shared<WireHandler>());
    client.send_tui_get("port", "5"); assert(processor.process(in, out, nullptr));
    sai_tui::Object o; client.recv_tui_get(o); assert(o.kind == "port" && o.attributes.at("lanes") == "11,12");
    client.send_tui_get("port", "-1"); assert(processor.process(in, out, nullptr));
    error([&] { client.recv_tui_get(o); }, SAI_STATUS_INVALID_PARAMETER);
    failcreate = true;
    client.send_tui_create("vlan", {{"vlan_id", "77"}}); assert(processor.process(in, out, nullptr));
    error([&] { client.recv_tui_create(o); }, SAI_STATUS_TABLE_FULL);
    failcreate = false;
}
} // namespace
extern "C" sai_status_t sai_api_query(sai_api_t id, void** table) {
    ++queries;
    if (query_status != SAI_STATUS_SUCCESS) return query_status;
    switch (id) {
    case SAI_API_PORT: *table = &ports; break;
    case SAI_API_VLAN: *table = &vlans; break;
    case SAI_API_BRIDGE: *table = &bridges; break;
    case SAI_API_VIRTUAL_ROUTER: *table = &vrs; break;
    case SAI_API_ROUTER_INTERFACE: *table = &rifs; break;
    case SAI_API_NEXT_HOP: *table = &nhs; break;
    case SAI_API_NEIGHBOR: *table = &neighbors; break;
    case SAI_API_ROUTE: *table = &routes; break;
    case SAI_API_ACL: *table = &acls; break;
    case SAI_API_SWITCH: *table = &switches; break;
    case SAI_API_FDB: *table = &fdb; break;
    default: return SAI_STATUS_NOT_SUPPORTED;
    }
    return SAI_STATUS_SUCCESS;
}
int main() {
    init(); validation(); crud(); failures(); inventory_counters(); wire();
    std::cout << "PASS: bounded CRUD IPv4/IPv6/L3/ACL, strict prevalidation, hardware readback, partial failures, discovery, counter subsets, inherited binary Thrift errors\n";
}
