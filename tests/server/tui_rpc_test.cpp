#include "src/tui_rpc.h"
#include "switch_sai_rpc.h"
extern "C" {
#include <sai.h>
}
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/transport/TBufferTransports.h>
#include <arpa/inet.h>
#include <cassert>
#include <algorithm>
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
std::map<sai_object_id_t, Record> deleted;
std::map<std::string, Record> entries;
uint64_t nextid = 100;
unsigned queries = 0, mutations = 0, gets = 0, writes = 0;
sai_attr_id_t failget = UINT32_MAX;
std::string failget_kind;
sai_status_t failget_status = SAI_STATUS_NOT_SUPPORTED;
sai_status_t remove_status = SAI_STATUS_SUCCESS;
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
        if (r.kind == "port" && a[i].id == SAI_PORT_ATTR_EGRESS_MIRROR_SESSION) {
            const auto& list = a[i].value.objlist;
            r.lists[a[i].id] = list.count ? std::vector<sai_object_id_t>(list.list, list.list + list.count) : std::vector<sai_object_id_t>{};
            continue;
        }
        r.values[a[i].id] = a[i].value;
    }
}
sai_status_t create(const char* kind, sai_object_id_t* id, uint32_t n, const sai_attribute_t* a) {
    ++mutations; if (failcreate) return SAI_STATUS_TABLE_FULL;
    *id = nextid++; records[*id].kind = kind; store(records[*id], n, a);
    if (std::string(kind) == "bridge_port") records.at(4).lists[SAI_BRIDGE_ATTR_PORT_LIST].push_back(*id);
    if (std::string(kind) == "acl_group") records[*id].lists[SAI_ACL_TABLE_GROUP_ATTR_MEMBER_LIST] = {};
    if (std::string(kind) == "acl_group_member") {
        auto parent = records[*id].values.at(SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_GROUP_ID).oid;
        records.at(parent).lists[SAI_ACL_TABLE_GROUP_ATTR_MEMBER_LIST].push_back(*id);
    }
    return SAI_STATUS_SUCCESS;
}
sai_status_t read(Record& r, uint32_t n, sai_attribute_t* a) {
    ++gets; assert(n == 1);
    if (a->id == failget && (failget_kind.empty() || failget_kind == r.kind)) return failget_status;
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
    if (wrongread && r.kind == "mirror_session" && a->id == SAI_MIRROR_SESSION_ATTR_TTL) a->value.u8 = 42;
    if (wrongread && r.kind == "port" && a->id == SAI_PORT_ATTR_SPEED) a->value.u32 = 25000;
    return SAI_STATUS_SUCCESS;
}
sai_status_t getoid(sai_object_id_t id, uint32_t n, sai_attribute_t* a) {
    if (forced_get_status != SAI_STATUS_SUCCESS) return forced_get_status;
    if (!records.count(id)) {
        // The identity getter can succeed after deletion; other actual
        // attributes correctly report absence. A single-field probe is unsafe.
        if (deleted.count(id) && deleted.at(id).kind == "vlan_member" && a->id == SAI_VLAN_MEMBER_ATTR_VLAN_ID)
            return read(deleted.at(id), n, a);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    return read(records.at(id), n, a);
}
sai_status_t setoid(sai_object_id_t id, const sai_attribute_t* a) {
    ++mutations; ++writes;
    if (writes == failwrite) return SAI_STATUS_OBJECT_IN_USE;
    if (!records.count(id)) return SAI_STATUS_ITEM_NOT_FOUND;
    store(records[id], 1, a); return SAI_STATUS_SUCCESS;
}
sai_status_t removeoid(sai_object_id_t id) {
    ++mutations; if (remove_status != SAI_STATUS_SUCCESS) return remove_status;
    if (!records.count(id)) return SAI_STATUS_ITEM_NOT_FOUND;
    if (!keepremoved) {
        if (records.at(id).kind == "acl_group_member") {
            auto parent = records.at(id).values.at(SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_GROUP_ID).oid;
            auto& members = records.at(parent).lists[SAI_ACL_TABLE_GROUP_ATTR_MEMBER_LIST];
            members.erase(std::remove(members.begin(), members.end(), id), members.end());
            // Model the real SDK quirk: its member getter keeps decoding stale
            // OID attributes after removal; only parent membership is reliable.
        } else if (records.at(id).kind == "bridge_port") {
            auto& members = records.at(4).lists[SAI_BRIDGE_ATTR_PORT_LIST];
            members.erase(std::remove(members.begin(), members.end(), id), members.end());
            // Retain decodable identity fields to model the real stale getter.
        } else { deleted[id] = records.at(id); records.erase(id); }
    }
    return SAI_STATUS_SUCCESS;
}
#define CREATOR(NAME) sai_status_t create_##NAME(sai_object_id_t* id, sai_object_id_t sw, uint32_t n, const sai_attribute_t* a) { assert(sw == 1); return create(#NAME, id, n, a); }
CREATOR(port) CREATOR(vlan) CREATOR(vlan_member) CREATOR(bridge_port) CREATOR(virtual_router)
CREATOR(mirror_session) CREATOR(router_interface) CREATOR(next_hop) CREATOR(acl_table) CREATOR(acl_entry) CREATOR(acl_group) CREATOR(acl_group_member)
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
sai_status_t gn(const sai_neighbor_entry_t* e, uint32_t n, sai_attribute_t* a) { if (forced_get_status != SAI_STATUS_SUCCESS) return forced_get_status; return entries.count(nk(e)) ? read(entries.at(nk(e)), n, a) : SAI_STATUS_ITEM_NOT_FOUND; }
sai_status_t gr(const sai_route_entry_t* e, uint32_t n, sai_attribute_t* a) { if (forced_get_status != SAI_STATUS_SUCCESS) return forced_get_status; return entries.count(rk(e)) ? read(entries.at(rk(e)), n, a) : SAI_STATUS_ITEM_NOT_FOUND; }
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
sai_switch_api_t switches{}; sai_fdb_api_t fdb{}; sai_mirror_api_t mirrors{};
void init() {
#define BIND(TABLE, NAME, CREATE) TABLE.create_##NAME = CREATE; TABLE.remove_##NAME = removeoid; TABLE.set_##NAME##_attribute = setoid; TABLE.get_##NAME##_attribute = getoid
    BIND(mirrors, mirror_session, create_mirror_session);
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
    records[5].kind = "port"; records[5].lists[SAI_PORT_ATTR_EGRESS_MIRROR_SESSION] = {};
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
    error([&] { tui_rpc::set(o, 1, "port", "5", {{"speed", "0"}}); }, SAI_STATUS_INVALID_PARAMETER);
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
void preset_mirrors() {
    sai_tui::Object o;
    const Attrs spec = {{"monitor_port", "5"}, {"src_ip", "192.0.2.1"}, {"dst_ip", "198.51.100.2"},
        {"src_mac", "02:00:00:00:00:01"}, {"dst_mac", "02:00:00:00:00:02"}, {"ttl", "64"}, {"tos", "16"}};
    auto bad = [&](const Attrs& a) {
        auto before = queries;
        error([&] { tui_rpc::create(o, 1, "mirror_session", a); }, SAI_STATUS_INVALID_PARAMETER);
        assert(queries == before);
    };
    for (const auto& kv : spec) { auto a = spec; a.erase(kv.first); bad(a); }
    for (const auto& kv : Attrs{{"src_ip", "::1"}, {"dst_ip", "1.2.3.999"}, {"src_mac", "0:00:00:00:00:01"},
            {"dst_mac", "xx:00:00:00:00:02"}, {"monitor_port", "0"}, {"ttl", "256"}, {"tos", "-1"},
            {"type", "local"}, {"encap_type", "l3_gre"}, {"gre_protocol", "35006"}, {"unknown", "1"}}) {
        auto a = spec; a[kv.first] = kv.second; bad(a);
    }
    auto before = mutations;
    failcreate = true; error([&] { tui_rpc::create(o, 1, "mirror_session", spec); }, SAI_STATUS_TABLE_FULL);
    assert(mutations == before + 1); failcreate = false;
    query_status = SAI_STATUS_UNINITIALIZED;
    error([&] { tui_rpc::create(o, 1, "mirror_session", spec); }, SAI_STATUS_UNINITIALIZED);
    query_status = SAI_STATUS_SUCCESS;
    auto createfn = mirrors.create_mirror_session; mirrors.create_mirror_session = nullptr;
    error([&] { tui_rpc::create(o, 1, "mirror_session", spec); }, SAI_STATUS_NOT_SUPPORTED);
    mirrors.create_mirror_session = createfn;
    wrongread = true; auto m = make("mirror_session", spec); wrongread = false;
    assert(m.attributes.at("ttl") == "42"); // Not the requested 64.
    uint64_t id = std::stoull(m.key, nullptr, 16);
    auto& values = records.at(id).values;
    assert(values.at(SAI_MIRROR_SESSION_ATTR_TYPE).s32 == SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE);
    assert(values.at(SAI_MIRROR_SESSION_ATTR_ERSPAN_ENCAPSULATION_TYPE).s32 == SAI_ERSPAN_ENCAPSULATION_TYPE_MIRROR_L3_GRE_TUNNEL);
    assert(values.at(SAI_MIRROR_SESSION_ATTR_IPHDR_VERSION).u8 == 4);
    assert(values.at(SAI_MIRROR_SESSION_ATTR_GRE_PROTOCOL_TYPE).u16 == 0x88be);
    assert(!values.at(SAI_MIRROR_SESSION_ATTR_VLAN_HEADER_VALID).booldata && !values.at(SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST_VALID).booldata);
    assert(m.attributes.at("type") == "enhanced_remote" && m.attributes.at("encap_type") == "l3_gre");
    assert(m.attributes.at("ip_version") == "4" && m.attributes.at("gre_protocol") == "35006");
    Attrs update = {{"monitor_port", "6"}, {"src_ip", "203.0.113.1"}, {"dst_ip", "203.0.113.2"},
        {"src_mac", "02:11:22:33:44:55"}, {"dst_mac", "02:AA:BB:CC:DD:EE"}, {"ttl", "255"}, {"tos", "0"}};
    tui_rpc::set(o, 1, "mirror_session", m.key, update);
    for (const auto& kv : update) if (kv.first != "monitor_port" && kv.first != "dst_mac") assert(o.attributes.at(kv.first) == kv.second);
    assert(o.attributes.at("monitor_port") == "0x6" && o.attributes.at("dst_mac") == "02:aa:bb:cc:dd:ee");
    before = queries;
    for (const char* name : {"type", "encap_type", "ip_version", "gre_protocol", "vlan_header_valid", "monitor_portlist_valid"})
        error([&] { tui_rpc::set(o, 1, "mirror_session", m.key, {{name, "1"}}); }, SAI_STATUS_INVALID_PARAMETER);
    assert(queries == before);
    for (auto attr : {SAI_MIRROR_SESSION_ATTR_TYPE, SAI_MIRROR_SESSION_ATTR_ERSPAN_ENCAPSULATION_TYPE,
            SAI_MIRROR_SESSION_ATTR_IPHDR_VERSION, SAI_MIRROR_SESSION_ATTR_GRE_PROTOCOL_TYPE,
            SAI_MIRROR_SESSION_ATTR_VLAN_HEADER_VALID, SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST_VALID,
            SAI_MIRROR_SESSION_ATTR_MONITOR_PORT, SAI_MIRROR_SESSION_ATTR_SRC_IP_ADDRESS, SAI_MIRROR_SESSION_ATTR_DST_IP_ADDRESS,
            SAI_MIRROR_SESSION_ATTR_SRC_MAC_ADDRESS, SAI_MIRROR_SESSION_ATTR_DST_MAC_ADDRESS, SAI_MIRROR_SESSION_ATTR_TTL, SAI_MIRROR_SESSION_ATTR_TOS}) {
        failget = attr; failget_status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0;
        error([&] { tui_rpc::get(o, 1, "mirror_session", m.key); }, SAI_STATUS_ATTR_NOT_IMPLEMENTED_0);
    }
    failget = UINT32_MAX; failget_status = SAI_STATUS_NOT_SUPPORTED;
    for (auto attr : {SAI_MIRROR_SESSION_ATTR_TYPE, SAI_MIRROR_SESSION_ATTR_ERSPAN_ENCAPSULATION_TYPE,
            SAI_MIRROR_SESSION_ATTR_IPHDR_VERSION, SAI_MIRROR_SESSION_ATTR_GRE_PROTOCOL_TYPE,
            SAI_MIRROR_SESSION_ATTR_VLAN_HEADER_VALID, SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST_VALID}) {
        auto saved = values.at(attr); values[attr].u32 = 99;
        // bool union members must hold a valid bool, even in the fake backend.
        if (attr == SAI_MIRROR_SESSION_ATTR_VLAN_HEADER_VALID || attr == SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST_VALID) values[attr].booldata = true;
        before = mutations;
        error([&] { tui_rpc::get(o, 1, "mirror_session", m.key); }, SAI_STATUS_NOT_SUPPORTED);
        error([&] { tui_rpc::set(o, 1, "mirror_session", m.key, {{"ttl", "1"}}); }, SAI_STATUS_NOT_SUPPORTED);
        assert(mutations == before); values[attr] = saved;
    }
    auto savedip = values.at(SAI_MIRROR_SESSION_ATTR_SRC_IP_ADDRESS);
    values[SAI_MIRROR_SESSION_ATTR_SRC_IP_ADDRESS].ipaddr.addr_family = SAI_IP_ADDR_FAMILY_IPV6;
    error([&] { tui_rpc::get(o, 1, "mirror_session", m.key); }, SAI_STATUS_NOT_SUPPORTED);
    values[SAI_MIRROR_SESSION_ATTR_SRC_IP_ADDRESS] = savedip;
    failwrite = writes + 2; before = mutations;
    error([&] { tui_rpc::set(o, 1, "mirror_session", m.key, {{"tos", "1"}, {"ttl", "2"}}); }, SAI_STATUS_OBJECT_IN_USE, "partial readback observed");
    assert(mutations == before + 2); failwrite = 0;
    failget = SAI_MIRROR_SESSION_ATTR_TTL;
    error([&] { tui_rpc::set(o, 1, "mirror_session", m.key, {{"ttl", "2"}}); }, SAI_STATUS_NOT_SUPPORTED, "READBACK FAILED");
    auto failedid = nextid;
    error([&] { tui_rpc::create(o, 1, "mirror_session", spec); }, SAI_STATUS_NOT_SUPPORTED, "READBACK FAILED");
    failget = UINT32_MAX;
    // Known-key and port-list discovery work even for a session not registered by the service.
    auto external = nextid++; records[external] = records.at(id);
    tui_rpc::get(o, 1, "mirror_session", h(external)); assert(o.key == h(external));
    tui_rpc::set(o, 1, "port", "5", {{"egress_mirror_sessions", m.key + "," + h(external)}});
    assert(o.attributes.at("egress_mirror_sessions") == m.key + "," + h(external));
    assert(records.at(5).lists.at(SAI_PORT_ATTR_EGRESS_MIRROR_SESSION) == (std::vector<sai_object_id_t>{id, external}));
    sai_tui::Inventory inv; tui_rpc::snapshot(inv, 1);
    for (auto expected : {id, external, failedid}) {
        assert(std::count_if(inv.objects.begin(), inv.objects.end(), [&](const sai_tui::Object& x) { return x.kind == "mirror_session" && x.key == h(expected); }) == 1);
    }
    failget = SAI_MIRROR_SESSION_ATTR_TTL; tui_rpc::snapshot(inv, 1);
    assert(std::none_of(inv.objects.begin(), inv.objects.end(), [](const sai_tui::Object& x) { return x.kind == "mirror_session"; }));
    assert(inv.warnings.size() >= 5); failget = UINT32_MAX;
    before = queries;
    for (const char* list : {"0", "1,", ",1", "1,,2", "1, 2", "1,0x1", "-1", "0xg"})
        error([&] { tui_rpc::set(o, 1, "port", "5", {{"admin", "true"}, {"egress_mirror_sessions", list}}); }, SAI_STATUS_INVALID_PARAMETER);
    for (const char* speed : {"0", "-1", "100G", "4294967296", " 10000"})
        error([&] { tui_rpc::set(o, 1, "port", "5", {{"speed", speed}}); }, SAI_STATUS_INVALID_PARAMETER);
    std::string huge;
    for (unsigned i = 1; i <= 65537; ++i) { if (!huge.empty()) huge += ','; huge += std::to_string(i); }
    error([&] { tui_rpc::set(o, 1, "port", "5", {{"egress_mirror_sessions", huge}}); }, SAI_STATUS_INVALID_PARAMETER);
    assert(queries == before);
    // Readback follows external changes too; no requested-list cache.
    records.at(5).lists[SAI_PORT_ATTR_EGRESS_MIRROR_SESSION] = {external};
    tui_rpc::get(o, 1, "port", "5"); assert(o.attributes.at("egress_mirror_sessions") == h(external));
    wrongread = true; tui_rpc::set(o, 1, "port", "5", {{"speed", "10000"}}); wrongread = false;
    assert(records.at(5).values.at(SAI_PORT_ATTR_SPEED).u32 == 10000 && o.attributes.at("speed") == "25000");
    for (const char* name : {"speed", "egress_mirror_sessions"}) {
        failwrite = writes + 1;
        error([&] { tui_rpc::set(o, 1, "port", "5", {{name, "123"}}); }, SAI_STATUS_OBJECT_IN_USE);
        failwrite = 0;
    }
    failget = SAI_PORT_ATTR_EGRESS_MIRROR_SESSION;
    tui_rpc::get(o, 1, "port", "5");
    assert(o.attributes.count("lanes") && !o.attributes.count("egress_mirror_sessions"));
    assert(o.attributes.at("unavailable.egress_mirror_sessions").find("status") != std::string::npos);
    error([&] { tui_rpc::set(o, 1, "port", "5", {{"egress_mirror_sessions", ""}}); }, SAI_STATUS_NOT_SUPPORTED, "READBACK FAILED");
    tui_rpc::get(o, 1, "port", "5");
    assert(o.attributes.count("unavailable.egress_mirror_sessions"));
    failget = UINT32_MAX;
    tui_rpc::set(o, 1, "port", "5", {{"egress_mirror_sessions", ""}}); assert(o.attributes.at("egress_mirror_sessions").empty());
    tui_rpc::set(o, 1, "port", "5", {{"drop_tagged", "true"}, {"drop_untagged", "false"}});
    assert(o.attributes.at("drop_tagged") == "true" && o.attributes.at("drop_untagged") == "false");
    assert(records.at(5).values.at(SAI_PORT_ATTR_DROP_TAGGED).booldata);
    assert(!records.at(5).values.at(SAI_PORT_ATTR_DROP_UNTAGGED).booldata);
    error([&] { tui_rpc::set(o, 1, "port", "5", {{"drop_tagged", "invalid"}}); }, SAI_STATUS_INVALID_PARAMETER);
    remove_status = SAI_STATUS_OBJECT_IN_USE;
    error([&] { tui_rpc::remove(1, "mirror_session", m.key); }, SAI_STATUS_OBJECT_IN_USE);
    remove_status = SAI_STATUS_SUCCESS; keepremoved = true;
    error([&] { tui_rpc::remove(1, "mirror_session", m.key); }, SAI_STATUS_FAILURE, "still readable");
    keepremoved = false; forced_get_status = SAI_STATUS_FAILURE;
    auto saved = records.at(id);
    error([&] { tui_rpc::remove(1, "mirror_session", m.key); }, SAI_STATUS_FAILURE, "absence could not be confirmed");
    forced_get_status = SAI_STATUS_SUCCESS; records[id] = saved;
    for (auto gone : {id, external, failedid}) {
        tui_rpc::remove(1, "mirror_session", h(gone));
        error([&] { tui_rpc::get(o, 1, "mirror_session", h(gone)); }, SAI_STATUS_ITEM_NOT_FOUND);
    }
}
void preset_acls() {
    sai_tui::Object o;
    for (const char* family : {"ipv4", "ipv6", "mac"}) {
        bool mac = std::string(family) == "mac", v4 = std::string(family) == "ipv4";
        auto t = make("acl_table", {{"stage", "ingress"}, {"family", family}, {"src_mac_enabled", "true"}, {"l4_dst_port_enabled", mac ? "false" : "true"}});
        assert(t.attributes.at("family") == family && t.attributes.at("src_mac_enabled") == "true");
        assert(t.attributes.at("l4_dst_port_enabled") == (mac ? "false" : "true"));
        assert(t.attributes.at("src_enabled") == (mac ? "false" : "true") && t.attributes.at("protocol_enabled") == (mac ? "false" : "true"));
        auto tid = std::stoull(t.key, nullptr, 16);
        assert(records.at(tid).values.at(SAI_ACL_TABLE_ATTR_FIELD_SRC_MAC).booldata);
        Attrs spec = {{"table", t.key}, {"priority", "100"}, {"action", "deny"}, {"src_mac", "AA:BB:CC:DD:EE:FF"}};
        if (!mac) { spec["protocol"] = "6"; spec["l4_dst_port"] = "443"; }
        auto e = make("acl_entry", spec); auto eid = std::stoull(e.key, nullptr, 16);
        assert(e.attributes.at("src_mac") == "aa:bb:cc:dd:ee:ff" && e.attributes.at("action") == "deny");
        auto& vals = records.at(eid).values;
        auto& mf = vals.at(SAI_ACL_ENTRY_ATTR_FIELD_SRC_MAC).aclfield;
        assert(mf.enable && mf.data.mac[0] == 0xaa);
        for (auto byte : mf.mask.mac) assert(byte == 255);
        if (!mac) {
            assert(e.attributes.at("l4_dst_port") == "443");
            auto& port = vals.at(SAI_ACL_ENTRY_ATTR_FIELD_L4_DST_PORT).aclfield;
            assert(port.enable && port.data.u16 == 443 && port.mask.u16 == 65535);
            tui_rpc::set(o, 1, "acl_entry", e.key, {{"l4_dst_port", "65535"}}); assert(o.attributes.at("l4_dst_port") == "65535");
            auto before = mutations;
            error([&] { tui_rpc::set(o, 1, "acl_entry", e.key, {{"action", "permit"}, {"protocol", "17"}}); }, SAI_STATUS_INVALID_PARAMETER);
            assert(mutations == before);
            port.data.u16 = 22; tui_rpc::get(o, 1, "acl_entry", e.key); assert(o.attributes.at("l4_dst_port") == "22");
            port.mask.u16 = 255;
            error([&] { tui_rpc::get(o, 1, "acl_entry", e.key); }, SAI_STATUS_NOT_SUPPORTED, "non-exact mask"); port.mask.u16 = 65535;
            auto pid = v4 ? SAI_ACL_ENTRY_ATTR_FIELD_IP_PROTOCOL : SAI_ACL_ENTRY_ATTR_FIELD_IPV6_NEXT_HEADER;
            vals[pid].aclfield.data.u8 = 17;
            error([&] { tui_rpc::get(o, 1, "acl_entry", e.key); }, SAI_STATUS_NOT_SUPPORTED, "TCP");
            before = mutations;
            error([&] { tui_rpc::set(o, 1, "acl_entry", e.key, {{"l4_dst_port", "1"}}); }, SAI_STATUS_INVALID_PARAMETER, "TCP");
            assert(mutations == before); vals[pid].aclfield.data.u8 = 6;
            failget = SAI_ACL_ENTRY_ATTR_FIELD_L4_DST_PORT;
            error([&] { tui_rpc::get(o, 1, "acl_entry", e.key); }, SAI_STATUS_NOT_SUPPORTED); failget = UINT32_MAX;
        } else {
            // No IP/protocol/EtherType qualifiers: MAC matches include non-IP frames.
            assert(!e.attributes.count("protocol") && !e.attributes.count("src") && !e.attributes.count("dst"));
            assert(!vals.count(SAI_ACL_ENTRY_ATTR_FIELD_IP_PROTOCOL) && !vals.count(SAI_ACL_ENTRY_ATTR_FIELD_IPV6_NEXT_HEADER));
            auto before = mutations;
            error([&] { tui_rpc::set(o, 1, "acl_entry", e.key, {{"protocol", "6"}}); }, SAI_STATUS_NOT_SUPPORTED);
            error([&] { tui_rpc::set(o, 1, "acl_entry", e.key, {{"src", "0.0.0.0/0"}}); }, SAI_STATUS_NOT_SUPPORTED);
            assert(mutations == before);
        }
        tui_rpc::set(o, 1, "acl_entry", e.key, {{"src_mac", "02:00:00:00:00:01"}}); assert(o.attributes.at("src_mac") == "02:00:00:00:00:01");
        mf.data.mac[5] = 2; tui_rpc::get(o, 1, "acl_entry", e.key); assert(o.attributes.at("src_mac") == "02:00:00:00:00:02");
        mf.mask.mac[0] = 0;
        error([&] { tui_rpc::get(o, 1, "acl_entry", e.key); }, SAI_STATUS_NOT_SUPPORTED, "non-exact mask"); mf.mask.mac[0] = 255;
        failget = SAI_ACL_ENTRY_ATTR_FIELD_SRC_MAC; failget_kind = "acl_entry";
        error([&] { tui_rpc::set(o, 1, "acl_entry", e.key, {{"src_mac", "02:00:00:00:00:03"}}); }, SAI_STATUS_NOT_SUPPORTED, "READBACK FAILED");
        failget = UINT32_MAX; failget_kind.clear();
        failwrite = writes + 1;
        error([&] { tui_rpc::set(o, 1, "acl_entry", e.key, {{"src_mac", "02:00:00:00:00:04"}}); }, SAI_STATUS_OBJECT_IN_USE); failwrite = 0;
        mf.enable = false; tui_rpc::get(o, 1, "acl_entry", e.key); assert(!o.attributes.count("src_mac"));
        for (auto attr : {SAI_ACL_TABLE_ATTR_FIELD_SRC_MAC, SAI_ACL_TABLE_ATTR_FIELD_L4_DST_PORT}) {
            failget = attr;
            error([&] { tui_rpc::get(o, 1, "acl_table", t.key); }, SAI_STATUS_NOT_SUPPORTED);
            auto before = mutations;
            error([&] { tui_rpc::set(o, 1, "acl_entry", e.key, {{"action", "permit"}}); }, SAI_STATUS_NOT_SUPPORTED); assert(mutations == before);
        }
        failget = UINT32_MAX;
        tui_rpc::remove(1, "acl_entry", e.key); tui_rpc::remove(1, "acl_table", t.key);
    }
    auto before = queries;
    for (const auto& kv : std::vector<std::pair<std::string, std::string>>{{"src_mac", "02:00:00:00:00:01/48"}, {"l4_dst_port", "65536"}, {"l4_dst_port", "-1"}}) {
        Attrs a = {{"table", "10"}, {"priority", "1"}, {"action", "deny"}, {"protocol", "6"}}; a[kv.first] = kv.second;
        error([&] { tui_rpc::create(o, 1, "acl_entry", a); }, SAI_STATUS_INVALID_PARAMETER);
    }
    for (const char* protocol : {"", "17"}) {
        Attrs a = {{"table", "10"}, {"priority", "1"}, {"action", "deny"}, {"l4_dst_port", "443"}};
        if (*protocol) a["protocol"] = protocol;
        error([&] { tui_rpc::create(o, 1, "acl_entry", a); }, SAI_STATUS_INVALID_PARAMETER);
    }
    for (const auto& kv : Attrs{{"src_mac_enabled", "false"}, {"l4_dst_port_enabled", "true"}})
        error([&] { tui_rpc::create(o, 1, "acl_table", {{"stage", "ingress"}, {"family", "mac"}, kv}); }, SAI_STATUS_INVALID_PARAMETER);
    error([&] { tui_rpc::create(o, 1, "acl_table", {{"stage", "ingress"}, {"family", "ipv4"}, {"src_mac_enabled", "1"}}); }, SAI_STATUS_INVALID_PARAMETER);
    assert(queries == before);
    auto legacy = make("acl_table", {{"stage", "ingress"}, {"family", "ipv4"}});
    before = queries;
    for (const char* name : {"src_mac_enabled", "l4_dst_port_enabled"})
        error([&] { tui_rpc::set(o, 1, "acl_table", legacy.key, {{name, "true"}}); }, SAI_STATUS_INVALID_PARAMETER, "immutable");
    assert(queries == before);
    assert(legacy.attributes.at("src_mac_enabled") == "false" && legacy.attributes.at("l4_dst_port_enabled") == "false");
    for (const auto& kv : Attrs{{"src_mac", "02:00:00:00:00:01"}, {"l4_dst_port", "443"}}) {
        before = mutations;
        error([&] { tui_rpc::create(o, 1, "acl_entry", {{"table", legacy.key}, {"priority", "1"}, {"action", "deny"}, {"protocol", "6"}, kv}); }, SAI_STATUS_NOT_SUPPORTED);
        assert(mutations == before);
    }
    tui_rpc::remove(1, "acl_table", legacy.key);
    // Independent deny predicates in parallel tables: no implicit catchall permit
    // or conjunction added by this API. All resources and bindings are explicit.
    auto mac = make("acl_table", {{"stage", "ingress"}, {"family", "mac"}});
    auto tcp = make("acl_table", {{"stage", "ingress"}, {"family", "ipv4"}, {"l4_dst_port_enabled", "true"}});
    auto group = make("acl_group", {{"stage", "ingress"}});
    auto mm = make("acl_group_member", {{"group", group.key}, {"table", mac.key}, {"priority", "1"}});
    auto tm = make("acl_group_member", {{"group", group.key}, {"table", tcp.key}, {"priority", "2"}});
    before = mutations;
    auto me = make("acl_entry", {{"table", mac.key}, {"priority", "100"}, {"action", "deny"}, {"src_mac", "02:00:00:00:00:01"}});
    auto te = make("acl_entry", {{"table", tcp.key}, {"priority", "100"}, {"action", "deny"}, {"protocol", "6"}, {"l4_dst_port", "443"}});
    assert(mutations == before + 2 && !me.attributes.count("l4_dst_port") && !te.attributes.count("src_mac"));
    tui_rpc::set(o, 1, "port", "5", {{"ingress_acl", group.key}});
    tui_rpc::set(o, 1, "port", "5", {{"ingress_acl", "0"}});
    for (const auto& x : {te, me, tm, mm, group, tcp, mac}) tui_rpc::remove(1, x.kind, x.key);
    // Explicit default deny with independent permit predicates in one table:
    // no catchall permit, and no implicit conjunction of the two allow rules.
    auto allow = make("acl_table", {{"stage", "ingress"}, {"family", "ipv4"}, {"src_mac_enabled", "true"}, {"l4_dst_port_enabled", "true"}});
    before = mutations;
    auto am = make("acl_entry", {{"table", allow.key}, {"priority", "300"}, {"action", "permit"}, {"src_mac", "02:00:00:00:00:01"}});
    auto at = make("acl_entry", {{"table", allow.key}, {"priority", "200"}, {"action", "permit"}, {"protocol", "6"}, {"l4_dst_port", "0"}});
    auto deny = make("acl_entry", {{"table", allow.key}, {"priority", "1"}, {"action", "deny"}});
    assert(mutations == before + 3);
    assert(!am.attributes.count("protocol") && !am.attributes.count("l4_dst_port"));
    assert(!at.attributes.count("src_mac") && at.attributes.at("l4_dst_port") == "0");
    for (const char* name : {"src", "dst", "protocol", "src_mac", "l4_dst_port"}) assert(!deny.attributes.count(name));
    for (const auto& x : {deny, at, am, allow}) tui_rpc::remove(1, x.kind, x.key);
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
    failget = SAI_PORT_ATTR_INGRESS_ACL;
    tui_rpc::get(o, 1, "port", "5");
    assert(!o.attributes.count("ingress_acl") && o.attributes.count("unavailable.ingress_acl"));
    assert(o.attributes.count("admin") && o.attributes.count("lanes"));
    failget = UINT32_MAX;
    // Objects on a table lacking protocol support must not silently ignore protocol.
    auto t = make("acl_table", {{"family", "ipv4"}, {"stage", "egress"}});
    auto tid = std::stoull(t.key, nullptr, 16); records[tid].values[SAI_ACL_TABLE_ATTR_FIELD_IP_PROTOCOL].booldata = false;
    auto before = mutations;
    error([&] { tui_rpc::create(o, 1, "acl_entry", {{"table", t.key}, {"priority", "1"}, {"action", "deny"}, {"protocol", "6"}}); }, SAI_STATUS_NOT_SUPPORTED, "does not support protocol"); assert(mutations == before);
    tui_rpc::remove(1, "acl_table", t.key);
    // INVALID_OBJECT_ID can mean a missing parent on composite entries. A
    // successful remove followed by that getter error is NOT confirmed absence.
    auto route = make("route", {{"virtual_router", "3"}, {"prefix", "198.51.100.0/24"}, {"next_hop", "0"}, {"action", "drop"}});
    auto neighbor = make("neighbor", {{"router_interface", "9"}, {"ip", "192.0.2.2"}, {"mac", "02:00:00:00:00:02"}});
    auto saved_entries = entries;
    forced_get_status = SAI_STATUS_INVALID_OBJECT_ID;
    error([&] { tui_rpc::remove(1, "route", route.key); }, SAI_STATUS_INVALID_OBJECT_ID, "absence could not be confirmed");
    error([&] { tui_rpc::remove(1, "neighbor", neighbor.key); }, SAI_STATUS_INVALID_OBJECT_ID, "absence could not be confirmed");
    forced_get_status = SAI_STATUS_SUCCESS;
    // Restore the fake backend solely to clean the retained enumeration hints.
    entries = saved_entries;
    tui_rpc::remove(1, "route", route.key); tui_rpc::remove(1, "neighbor", neighbor.key);
    auto standalone = make("vlan", {{"vlan_id", "19"}});
    forced_get_status = SAI_STATUS_INVALID_OBJECT_ID;
    tui_rpc::remove(1, "vlan", standalone.key);
    forced_get_status = SAI_STATUS_SUCCESS;
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
extern "C" sai_status_t sai_api_uninitialize() { return SAI_STATUS_SUCCESS; }
extern "C" sai_status_t sai_api_query(sai_api_t id, void** table) {
    ++queries;
    if (query_status != SAI_STATUS_SUCCESS) return query_status;
    switch (id) {
    case SAI_API_MIRROR: *table = &mirrors; break;
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
    init(); validation(); crud(); preset_mirrors(); preset_acls(); failures(); inventory_counters(); wire();
    std::cout << "PASS: bounded CRUD IPv4/IPv6/L3/ACL/MAC/TCP/ERSPAN, mirror binding/speed, strict prevalidation, hardware readback, partial failures, discovery, counter subsets, inherited binary Thrift errors\n";
}
