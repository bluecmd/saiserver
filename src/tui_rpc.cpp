#include "tui_rpc.h"
extern "C" {
#include <sai.h>
}
#include <arpa/inet.h>
#include <algorithm>
#include <cstring>
#include <functional>
#include <iomanip>
#include <limits>
#include <mutex>
#include <set>
#include <sstream>
#include <vector>

namespace tui_rpc {
namespace {
using Attrs = std::map<std::string, std::string>;
std::mutex mutex;
// Enumeration hints only: no requested or observed attribute values are cached.
std::map<uint64_t, std::set<std::pair<std::string, std::string>>> managed;
[[noreturn]] void fail(sai_status_t status, const std::string& message) {
    sai_tui::RpcError e; e.status = status; e.message = message; throw e;
}
void check(sai_status_t s, const std::string& op) { if (s != SAI_STATUS_SUCCESS) fail(s, op); }
[[noreturn]] void invalid(const std::string& s) { fail(SAI_STATUS_INVALID_PARAMETER, s); }
std::string hex(uint64_t n) { std::ostringstream s; s << "0x" << std::hex << n; return s.str(); }
uint64_t number(const std::string& s, uint64_t max, bool oid = false) {
    size_t i = 0; unsigned base = 10;
    if (oid && s.size() > 2 && s[0] == '0' && s[1] == 'x') { base = 16; i = 2; }
    if (i == s.size() || s.empty() || s.size() > 32) invalid("invalid unsigned integer: " + s);
    uint64_t n = 0;
    for (; i < s.size(); ++i) {
        char c = s[i]; unsigned d = c >= '0' && c <= '9' ? c - '0' :
            c >= 'a' && c <= 'f' ? c - 'a' + 10 : c >= 'A' && c <= 'F' ? c - 'A' + 10 : 99;
        if (d >= base || d > max || n > (max - d) / base) invalid("invalid/out-of-range integer: " + s);
        n = n * base + d;
    }
    return n;
}
sai_object_id_t oid(const std::string& s, bool zero = false) {
    auto n = number(s, UINT64_MAX, true); if (!zero && !n) invalid("null OID is not allowed"); return n;
}
bool boolean(const std::string& s) { if (s == "true") return true; if (s == "false") return false; invalid("expected true/false: " + s); }
std::string boolean(bool b) { return b ? "true" : "false"; }
sai_ip_address_t ip(const std::string& s) {
    if (s.empty() || s.size() >= INET6_ADDRSTRLEN || s.find('\0') != std::string::npos) invalid("invalid IP address");
    sai_ip_address_t a{};
    if (inet_pton(AF_INET, s.c_str(), &a.addr.ip4) == 1) a.addr_family = SAI_IP_ADDR_FAMILY_IPV4;
    else if (inet_pton(AF_INET6, s.c_str(), a.addr.ip6) == 1) a.addr_family = SAI_IP_ADDR_FAMILY_IPV6;
    else invalid("invalid IP address: " + s);
    return a;
}
std::string iptext(const sai_ip_address_t& a) {
    char b[INET6_ADDRSTRLEN];
    if (a.addr_family != SAI_IP_ADDR_FAMILY_IPV4 && a.addr_family != SAI_IP_ADDR_FAMILY_IPV6)
        fail(SAI_STATUS_NOT_SUPPORTED, "getter returned unknown IP address family");
    const void* p = a.addr_family == SAI_IP_ADDR_FAMILY_IPV4 ? static_cast<const void*>(&a.addr.ip4) : a.addr.ip6;
    if (!inet_ntop(a.addr_family == SAI_IP_ADDR_FAMILY_IPV4 ? AF_INET : AF_INET6, p, b, sizeof(b)))
        fail(SAI_STATUS_FAILURE, "cannot format SAI IP address");
    return b;
}
sai_ip_prefix_t prefix(const std::string& s) {
    auto slash = s.find('/'); if (slash == std::string::npos) invalid("CIDR requires prefix length: " + s);
    auto a = ip(s.substr(0, slash)); unsigned bits = a.addr_family == SAI_IP_ADDR_FAMILY_IPV4 ? 32 : 128;
    unsigned n = number(s.substr(slash + 1), bits);
    sai_ip_prefix_t p{}; p.addr_family = a.addr_family; p.addr = a.addr;
    auto* mask = reinterpret_cast<uint8_t*>(&p.mask); auto* data = reinterpret_cast<uint8_t*>(&p.addr);
    for (unsigned i = 0; i < bits / 8; ++i) {
        mask[i] = n >= 8 ? 255 : n ? uint8_t(255 << (8 - n)) : 0;
        n = n >= 8 ? n - 8 : 0; data[i] &= mask[i];
    }
    return p;
}
std::string prefixtext(const sai_ip_prefix_t& p) {
    sai_ip_address_t a{}; a.addr_family = p.addr_family; a.addr = p.addr;
    unsigned bits = p.addr_family == SAI_IP_ADDR_FAMILY_IPV4 ? 32 : 128, n = 0; bool end = false;
    const auto* m = reinterpret_cast<const uint8_t*>(&p.mask);
    for (unsigned i = 0; i < bits; ++i) {
        bool bit = m[i / 8] & (128 >> (i % 8));
        if (bit && end) fail(SAI_STATUS_FAILURE, "getter returned noncontiguous IP mask");
        if (bit) ++n; else end = true;
    }
    return iptext(a) + "/" + std::to_string(n);
}
void mac(const std::string& s, uint8_t* out) {
    if (s.size() != 17) invalid("MAC must have six two-digit octets");
    for (unsigned i = 0; i < 6; ++i) {
        if (i && s[3*i-1] != ':') invalid("invalid MAC: " + s);
        out[i] = number("0x" + s.substr(3*i, 2), 255, true);
    }
}
std::string mactext(const uint8_t* p) {
    std::ostringstream s; s << std::hex << std::setfill('0');
    for (unsigned i = 0; i < 6; ++i) { if (i) s << ':'; s << std::setw(2) << unsigned(p[i]); } return s.str();
}
std::pair<std::string, std::string> splitkey(const std::string& s) {
    auto p = s.find('@'); if (p == std::string::npos || s.find('@', p+1) != std::string::npos) invalid("expected OID@address key");
    return {s.substr(0,p), s.substr(p+1)};
}
struct Key {
    sai_object_id_t id = 0;
    sai_neighbor_entry_t neighbor{}; sai_route_entry_t route{}; sai_fdb_entry_t fdb{};
    std::string text;
};
Key key(uint64_t sw, const std::string& kind, const std::string& text) {
    Key k;
    if (kind == "neighbor" || kind == "route" || kind == "fdb") {
        auto parts = splitkey(text); auto id = oid(parts.first);
        if (kind == "neighbor") { k.neighbor.switch_id = sw; k.neighbor.rif_id = id; k.neighbor.ip_address = ip(parts.second); k.text = hex(id) + "@" + iptext(k.neighbor.ip_address); }
        if (kind == "route") { k.route.switch_id = sw; k.route.vr_id = id; k.route.destination = prefix(parts.second); k.text = hex(id) + "@" + prefixtext(k.route.destination); }
        if (kind == "fdb") { k.fdb.switch_id = sw; k.fdb.bv_id = id; mac(parts.second, k.fdb.mac_address); k.text = hex(id) + "@" + mactext(k.fdb.mac_address); }
    } else { k.id = oid(text); k.text = hex(k.id); }
    return k;
}
template<class T> T* api(sai_api_t id) {
    T* p = nullptr; check(sai_api_query(id, reinterpret_cast<void**>(&p)), "SAI API query " + std::to_string(id));
    if (!p) fail(SAI_STATUS_NOT_SUPPORTED, "SAI API query returned null table");
    return p;
}
struct Ops {
    sai_create_vlan_fn create = nullptr;
    sai_remove_vlan_fn remove = nullptr;
    sai_set_vlan_attribute_fn set = nullptr;
    sai_get_vlan_attribute_fn get = nullptr;
};
Ops ops(const std::string& k) {
    Ops o;
#define OPS(K, API, TYPE, NAME) if (k == K) { auto p = api<TYPE>(API); o.create = p->create_##NAME; o.remove = p->remove_##NAME; o.set = p->set_##NAME##_attribute; o.get = p->get_##NAME##_attribute; return o; }
    OPS("port", SAI_API_PORT, sai_port_api_t, port)
    OPS("vlan", SAI_API_VLAN, sai_vlan_api_t, vlan)
    OPS("vlan_member", SAI_API_VLAN, sai_vlan_api_t, vlan_member)
    OPS("bridge_port", SAI_API_BRIDGE, sai_bridge_api_t, bridge_port)
    OPS("bridge", SAI_API_BRIDGE, sai_bridge_api_t, bridge)
    OPS("virtual_router", SAI_API_VIRTUAL_ROUTER, sai_virtual_router_api_t, virtual_router)
    OPS("router_interface", SAI_API_ROUTER_INTERFACE, sai_router_interface_api_t, router_interface)
    OPS("next_hop", SAI_API_NEXT_HOP, sai_next_hop_api_t, next_hop)
    OPS("acl_table", SAI_API_ACL, sai_acl_api_t, acl_table)
    OPS("acl_entry", SAI_API_ACL, sai_acl_api_t, acl_entry)
    OPS("acl_group", SAI_API_ACL, sai_acl_api_t, acl_table_group)
    OPS("acl_group_member", SAI_API_ACL, sai_acl_api_t, acl_table_group_member)
#undef OPS
    if (k == "switch") { auto p = api<sai_switch_api_t>(SAI_API_SWITCH); o.get = p->get_switch_attribute; return o; }
    invalid("unsupported kind: " + k);
}
void kindcheck(const std::string& k) {
    static const std::set<std::string> kinds = {"switch", "bridge", "port", "vlan", "bridge_port", "vlan_member", "virtual_router", "router_interface", "next_hop", "neighbor", "route", "acl_table", "acl_entry", "acl_group", "acl_group_member", "fdb"};
    if (!kinds.count(k)) invalid("unsupported kind: " + k);
}
sai_status_t rawget(const std::string& kind, const Key& k, sai_attribute_t* a) {
    if (kind == "neighbor") { auto p = api<sai_neighbor_api_t>(SAI_API_NEIGHBOR); return p->get_neighbor_entry_attribute ? p->get_neighbor_entry_attribute(&k.neighbor, 1, a) : SAI_STATUS_NOT_SUPPORTED; }
    if (kind == "route") { auto p = api<sai_route_api_t>(SAI_API_ROUTE); return p->get_route_entry_attribute ? p->get_route_entry_attribute(&k.route, 1, a) : SAI_STATUS_NOT_SUPPORTED; }
    if (kind == "fdb") { auto p = api<sai_fdb_api_t>(SAI_API_FDB); return p->get_fdb_entry_attribute ? p->get_fdb_entry_attribute(&k.fdb, 1, a) : SAI_STATUS_NOT_SUPPORTED; }
    auto o = ops(kind); return o.get ? o.get(k.id, 1, a) : SAI_STATUS_NOT_SUPPORTED;
}
sai_attribute_t read(const std::string& kind, const Key& k, sai_attr_id_t id) {
    sai_attribute_t a{}; a.id = id; check(rawget(kind, k, &a), "get " + kind + " " + k.text + " attr " + std::to_string(id)); return a;
}
std::vector<sai_object_id_t> list(const std::string& kind, const Key& k, sai_attr_id_t id) {
    std::vector<sai_object_id_t> v;
    for (unsigned tries = 0; tries < 4; ++tries) {
        sai_attribute_t a{}; a.id = id; a.value.objlist.count = v.size(); a.value.objlist.list = v.empty() ? nullptr : v.data();
        auto s = rawget(kind, k, &a);
        if (s == SAI_STATUS_SUCCESS) {
            if (a.value.objlist.count > v.size()) fail(SAI_STATUS_FAILURE, "SAI list count exceeds supplied capacity");
            v.resize(a.value.objlist.count); return v;
        }
        if (s != SAI_STATUS_BUFFER_OVERFLOW) check(s, "get list " + kind + " " + k.text + " attr " + std::to_string(id));
        if (a.value.objlist.count > 65536 || a.value.objlist.count <= v.size()) fail(SAI_STATUS_FAILURE, "invalid/oversized SAI list size");
        v.resize(a.value.objlist.count);
    }
    fail(SAI_STATUS_FAILURE, "SAI list changed repeatedly during read");
}
std::string oidlist(const std::vector<sai_object_id_t>& v) {
    std::string s; for (auto id : v) { if (!s.empty()) s += ','; s += hex(id); } return s;
}
enum Type { BOOL, U8, U16, U32, OID, NULL_OID, MAC, IP, STAGE, LEARNING, TAGGING, ROUTE_ACTION, ACL_ACTION, MATCH4, MATCH6, PROTOCOL, INT };
struct Field { const char* name; sai_attr_id_t id; Type type; bool writable; bool required; };
std::vector<Field> fields(const std::string& k) {
#define F(N, ID, T, W, R) {N, ID, T, W, R}
    if (k == "port") return {F("admin", SAI_PORT_ATTR_ADMIN_STATE, BOOL, true, false), F("pvid", SAI_PORT_ATTR_PORT_VLAN_ID, U16, true, false), F("ingress_acl", SAI_PORT_ATTR_INGRESS_ACL, NULL_OID, true, false), F("egress_acl", SAI_PORT_ATTR_EGRESS_ACL, NULL_OID, true, false), F("speed", SAI_PORT_ATTR_SPEED, U32, false, false), F("oper_status", SAI_PORT_ATTR_OPER_STATUS, INT, false, false)};
    if (k == "vlan") return {F("vlan_id", SAI_VLAN_ATTR_VLAN_ID, U16, false, true)};
    if (k == "bridge_port") return {F("port", SAI_BRIDGE_PORT_ATTR_PORT_ID, OID, false, true), F("bridge", SAI_BRIDGE_PORT_ATTR_BRIDGE_ID, OID, false, false), F("admin", SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, BOOL, true, false), F("learning", SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_MODE, LEARNING, true, false)};
    if (k == "vlan_member") return {F("vlan", SAI_VLAN_MEMBER_ATTR_VLAN_ID, OID, false, true), F("bridge_port", SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID, OID, false, true), F("tagging", SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE, TAGGING, true, true)};
    if (k == "virtual_router") return {F("ipv4", SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V4_STATE, BOOL, true, false), F("ipv6", SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V6_STATE, BOOL, true, false)};
    if (k == "router_interface") return {F("virtual_router", SAI_ROUTER_INTERFACE_ATTR_VIRTUAL_ROUTER_ID, OID, false, true), F("port", SAI_ROUTER_INTERFACE_ATTR_PORT_ID, OID, false, false), F("vlan", SAI_ROUTER_INTERFACE_ATTR_VLAN_ID, OID, false, false), F("src_mac", SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS, MAC, true, false), F("mtu", SAI_ROUTER_INTERFACE_ATTR_MTU, U32, true, false), F("ipv4", SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE, BOOL, true, false), F("ipv6", SAI_ROUTER_INTERFACE_ATTR_ADMIN_V6_STATE, BOOL, true, false)};
    if (k == "next_hop") return {F("router_interface", SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID, OID, false, true), F("ip", SAI_NEXT_HOP_ATTR_IP, IP, false, true)};
    if (k == "neighbor") return {F("mac", SAI_NEIGHBOR_ENTRY_ATTR_DST_MAC_ADDRESS, MAC, true, true)};
    if (k == "route") return {F("next_hop", SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID, NULL_OID, true, true), F("action", SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, ROUTE_ACTION, true, false)};
    if (k == "acl_table") return {F("stage", SAI_ACL_TABLE_ATTR_ACL_STAGE, STAGE, false, true)};
    if (k == "acl_entry") return {F("table", SAI_ACL_ENTRY_ATTR_TABLE_ID, OID, false, true), F("priority", SAI_ACL_ENTRY_ATTR_PRIORITY, U32, true, true), F("enable", SAI_ACL_ENTRY_ATTR_ADMIN_STATE, BOOL, true, false), F("action", SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION, ACL_ACTION, true, true)};
    if (k == "acl_group") return {F("stage", SAI_ACL_TABLE_GROUP_ATTR_ACL_STAGE, STAGE, false, true)};
    if (k == "acl_group_member") return {F("group", SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_GROUP_ID, OID, false, true), F("table", SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_ID, OID, false, true), F("priority", SAI_ACL_TABLE_GROUP_MEMBER_ATTR_PRIORITY, U32, false, true)};
    if (k == "fdb") return {F("bridge_port", SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID, OID, false, false), F("type", SAI_FDB_ENTRY_ATTR_TYPE, INT, false, false)};
    if (k == "switch") return {F("default_vlan", SAI_SWITCH_ATTR_DEFAULT_VLAN_ID, OID, false, false), F("default_virtual_router", SAI_SWITCH_ATTR_DEFAULT_VIRTUAL_ROUTER_ID, OID, false, false), F("default_bridge", SAI_SWITCH_ATTR_DEFAULT_1Q_BRIDGE_ID, OID, false, false), F("src_mac", SAI_SWITCH_ATTR_SRC_MAC_ADDRESS, MAC, false, false)};
    return {};
#undef F
}
int32_t choice(const std::string& s, const char* a, int32_t av, const char* b, int32_t bv) {
    if (s == a) return av;
    if (s == b) return bv;
    invalid("expected " + std::string(a) + "/" + b + ": " + s);
}
sai_attribute_t encode(const Field& f, const std::string& s) {
    sai_attribute_t a{}; a.id = f.id;
    switch (f.type) {
    case BOOL: a.value.booldata = boolean(s); break;
    case U8: a.value.u8 = number(s, 255); break;
    case U16: a.value.u16 = number(s, 4094); if (!a.value.u16) invalid("VLAN ID/PVID must be 1..4094"); break;
    case U32: a.value.u32 = number(s, UINT32_MAX); if (std::string(f.name) == "mtu" && !a.value.u32) invalid("MTU must be positive"); break;
    case OID: case NULL_OID: a.value.oid = oid(s, f.type == NULL_OID); break;
    case MAC: mac(s, a.value.mac); break;
    case IP: a.value.ipaddr = ip(s); break;
    case STAGE: a.value.s32 = choice(s, "ingress", SAI_ACL_STAGE_INGRESS, "egress", SAI_ACL_STAGE_EGRESS); break;
    case LEARNING: a.value.s32 = choice(s, "hardware", SAI_BRIDGE_PORT_FDB_LEARNING_MODE_HW, "disable", SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DISABLE); break;
    case TAGGING: a.value.s32 = choice(s, "tagged", SAI_VLAN_TAGGING_MODE_TAGGED, "untagged", SAI_VLAN_TAGGING_MODE_UNTAGGED); break;
    case ROUTE_ACTION: a.value.s32 = choice(s, "forward", SAI_PACKET_ACTION_FORWARD, "drop", SAI_PACKET_ACTION_DROP); break;
    case ACL_ACTION: a.value.aclaction.enable = true; a.value.aclaction.parameter.s32 = choice(s, "permit", SAI_PACKET_ACTION_FORWARD, "deny", SAI_PACKET_ACTION_DROP); break;
    case MATCH4: case MATCH6: {
        auto p = prefix(s); if ((p.addr_family == SAI_IP_ADDR_FAMILY_IPV4) != (f.type == MATCH4)) invalid("ACL match address family disagrees with table");
        a.value.aclfield.enable = true;
        if (f.type == MATCH4) { a.value.aclfield.data.ip4 = p.addr.ip4; a.value.aclfield.mask.ip4 = p.mask.ip4; }
        else { std::memcpy(a.value.aclfield.data.ip6, p.addr.ip6, 16); std::memcpy(a.value.aclfield.mask.ip6, p.mask.ip6, 16); }
        break;
    }
    case PROTOCOL: a.value.aclfield.enable = true; a.value.aclfield.data.u8 = number(s, 255); a.value.aclfield.mask.u8 = 255; break;
    default: invalid("read-only attribute: " + std::string(f.name));
    }
    return a;
}
std::string decode(const Field& f, const sai_attribute_t& a) {
    switch (f.type) {
    case BOOL: return boolean(a.value.booldata);
    case U8: return std::to_string(a.value.u8);
    case U16: return std::to_string(a.value.u16);
    case U32: return std::to_string(a.value.u32);
    case OID: case NULL_OID: return hex(a.value.oid);
    case MAC: return mactext(a.value.mac);
    case IP: return iptext(a.value.ipaddr);
    case INT: return std::to_string(a.value.s32);
    case STAGE: if (a.value.s32 == SAI_ACL_STAGE_INGRESS) return "ingress"; if (a.value.s32 == SAI_ACL_STAGE_EGRESS) return "egress"; break;
    case LEARNING: if (a.value.s32 == SAI_BRIDGE_PORT_FDB_LEARNING_MODE_HW) return "hardware"; if (a.value.s32 == SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DISABLE) return "disable"; break;
    case TAGGING: if (a.value.s32 == SAI_VLAN_TAGGING_MODE_TAGGED) return "tagged"; if (a.value.s32 == SAI_VLAN_TAGGING_MODE_UNTAGGED) return "untagged"; break;
    case ROUTE_ACTION: if (a.value.s32 == SAI_PACKET_ACTION_FORWARD) return "forward"; if (a.value.s32 == SAI_PACKET_ACTION_DROP) return "drop"; break;
    case ACL_ACTION:
        if (!a.value.aclaction.enable) return "disabled";
        if (a.value.aclaction.parameter.s32 == SAI_PACKET_ACTION_FORWARD) return "permit";
        if (a.value.aclaction.parameter.s32 == SAI_PACKET_ACTION_DROP) return "deny";
        return std::to_string(a.value.aclaction.parameter.s32);
    case MATCH4: case MATCH6: {
        sai_ip_prefix_t p{}; p.addr_family = f.type == MATCH4 ? SAI_IP_ADDR_FAMILY_IPV4 : SAI_IP_ADDR_FAMILY_IPV6;
        if (f.type == MATCH4) { p.addr.ip4 = a.value.aclfield.data.ip4; p.mask.ip4 = a.value.aclfield.mask.ip4; }
        else { std::memcpy(p.addr.ip6, a.value.aclfield.data.ip6, 16); std::memcpy(p.mask.ip6, a.value.aclfield.mask.ip6, 16); }
        return prefixtext(p);
    }
    case PROTOCOL:
        if (a.value.aclfield.mask.u8 != 255) fail(SAI_STATUS_NOT_SUPPORTED, "existing ACL protocol uses non-exact mask; outside bounded u8 protocol match");
        return std::to_string(a.value.aclfield.data.u8);
    }
    // Additional enum values on existing objects are observations, not writable symbols.
    return std::to_string(a.value.s32);
}
struct Family { bool v4; bool v6; bool src; bool dst; bool protocol; };
Family tablefamily(const Key& k) {
    bool s4 = read("acl_table", k, SAI_ACL_TABLE_ATTR_FIELD_SRC_IP).value.booldata;
    bool d4 = read("acl_table", k, SAI_ACL_TABLE_ATTR_FIELD_DST_IP).value.booldata;
    bool s6 = read("acl_table", k, SAI_ACL_TABLE_ATTR_FIELD_SRC_IPV6).value.booldata;
    bool d6 = read("acl_table", k, SAI_ACL_TABLE_ATTR_FIELD_DST_IPV6).value.booldata;
    bool proto = read("acl_table", k, (s6 || d6) && !(s4 || d4) ? SAI_ACL_TABLE_ATTR_FIELD_IPV6_NEXT_HEADER : SAI_ACL_TABLE_ATTR_FIELD_IP_PROTOCOL).value.booldata;
    return {s4 || d4, s6 || d6, s4 || s6, d4 || d6, proto};
}
std::vector<Field> matchfields(const Family& f) {
    if (f.v4 == f.v6) fail(SAI_STATUS_NOT_SUPPORTED, "ACL table must enable a single IPv4/IPv6 family for bounded entry management");
    std::vector<Field> fs;
    if (f.src) fs.push_back({"src", f.v4 ? SAI_ACL_ENTRY_ATTR_FIELD_SRC_IP : SAI_ACL_ENTRY_ATTR_FIELD_SRC_IPV6, f.v4 ? MATCH4 : MATCH6, true, false});
    if (f.dst) fs.push_back({"dst", f.v4 ? SAI_ACL_ENTRY_ATTR_FIELD_DST_IP : SAI_ACL_ENTRY_ATTR_FIELD_DST_IPV6, f.v4 ? MATCH4 : MATCH6, true, false});
    if (f.protocol) fs.push_back({"protocol", f.v4 ? SAI_ACL_ENTRY_ATTR_FIELD_IP_PROTOCOL : SAI_ACL_ENTRY_ATTR_FIELD_IPV6_NEXT_HEADER, PROTOCOL, true, false});
    return fs;
}
sai_tui::Object observe(uint64_t sw, const std::string& kind, const Key& k) {
    sai_tui::Object out; out.kind = kind; out.key = k.text;
    auto fs = fields(kind);
    int32_t type = -1;
    if (kind == "router_interface") { type = read(kind, k, SAI_ROUTER_INTERFACE_ATTR_TYPE).value.s32; out.attributes["type"] = std::to_string(type); }
    if (kind == "bridge_port") { type = read(kind, k, SAI_BRIDGE_PORT_ATTR_TYPE).value.s32; out.attributes["type"] = std::to_string(type); }
    if (kind == "next_hop") {
        type = read(kind, k, SAI_NEXT_HOP_ATTR_TYPE).value.s32; out.attributes["type"] = std::to_string(type);
        if (type != SAI_NEXT_HOP_TYPE_IP) fail(SAI_STATUS_NOT_SUPPORTED, "only IP next hops are supported");
    }
    for (auto& f : fs) {
        std::string name = f.name;
        if (kind == "router_interface" && ((name == "port" && type != SAI_ROUTER_INTERFACE_TYPE_PORT) || (name == "vlan" && type != SAI_ROUTER_INTERFACE_TYPE_VLAN) || (name == "src_mac" && type == SAI_ROUTER_INTERFACE_TYPE_LOOPBACK))) continue;
        if (kind == "bridge_port" && name == "port" && type != SAI_BRIDGE_PORT_TYPE_PORT && type != SAI_BRIDGE_PORT_TYPE_SUB_PORT) continue;
        if (kind == "bridge_port" && name == "bridge" && (type == SAI_BRIDGE_PORT_TYPE_PORT || type == SAI_BRIDGE_PORT_TYPE_1Q_ROUTER)) continue;
        out.attributes[name] = decode(f, read(kind, k, f.id));
    }
    if (kind == "neighbor") { out.attributes["router_interface"] = hex(k.neighbor.rif_id); out.attributes["ip"] = iptext(k.neighbor.ip_address); }
    if (kind == "route") { out.attributes["virtual_router"] = hex(k.route.vr_id); out.attributes["prefix"] = prefixtext(k.route.destination); }
    if (kind == "fdb") { out.attributes["vlan"] = hex(k.fdb.bv_id); out.attributes["mac"] = mactext(k.fdb.mac_address); }
    if (kind == "vlan") out.attributes["members"] = oidlist(list(kind, k, SAI_VLAN_ATTR_MEMBER_LIST));
    if (kind == "bridge") { out.attributes["type"] = std::to_string(read(kind, k, SAI_BRIDGE_ATTR_TYPE).value.s32); out.attributes["ports"] = oidlist(list(kind, k, SAI_BRIDGE_ATTR_PORT_LIST)); }
    if (kind == "bridge_port" && (type == SAI_BRIDGE_PORT_TYPE_PORT || type == SAI_BRIDGE_PORT_TYPE_1Q_ROUTER))
        out.attributes["bridge"] = hex(read("switch", key(sw, "switch", hex(sw)), SAI_SWITCH_ATTR_DEFAULT_1Q_BRIDGE_ID).value.oid);
    if (kind == "bridge_port" && type == SAI_BRIDGE_PORT_TYPE_1D_ROUTER) out.attributes["router_interface"] = hex(read(kind, k, SAI_BRIDGE_PORT_ATTR_RIF_ID).value.oid);
    if (kind == "port") {
        std::vector<uint32_t> lanes;
        bool done = false;
        for (unsigned tries = 0; tries < 4; ++tries) {
            sai_attribute_t a{}; a.id = SAI_PORT_ATTR_HW_LANE_LIST; a.value.u32list.count = lanes.size(); a.value.u32list.list = lanes.empty() ? nullptr : lanes.data();
            auto s = rawget(kind, k, &a);
            if (s == SAI_STATUS_SUCCESS) { if (a.value.u32list.count > lanes.size()) fail(SAI_STATUS_FAILURE, "invalid lane list size"); lanes.resize(a.value.u32list.count); done = true; break; }
            if (s != SAI_STATUS_BUFFER_OVERFLOW) check(s, "get port lanes");
            if (a.value.u32list.count > 65536 || a.value.u32list.count <= lanes.size()) fail(SAI_STATUS_FAILURE, "invalid lane list size");
            lanes.resize(a.value.u32list.count);
        }
        if (!done) fail(SAI_STATUS_FAILURE, "port lanes changed repeatedly");
        std::string text; for (auto n : lanes) { if (!text.empty()) text += ','; text += std::to_string(n); } out.attributes["lanes"] = text;
    }
    if (kind == "acl_table") {
        auto f = tablefamily(k); out.attributes["family"] = f.v4 && !f.v6 ? "ipv4" : f.v6 && !f.v4 ? "ipv6" : "mixed-or-unspecified";
        out.attributes["src_enabled"] = boolean(f.src); out.attributes["dst_enabled"] = boolean(f.dst); out.attributes["protocol_enabled"] = boolean(f.protocol);
    }
    if (kind == "acl_group") out.attributes["type"] = std::to_string(read(kind, k, SAI_ACL_TABLE_GROUP_ATTR_TYPE).value.s32);
    if (kind == "acl_entry") {
        auto table = key(sw, "acl_table", out.attributes.at("table"));
        for (const auto& f : matchfields(tablefamily(table))) {
            auto a = read(kind, k, f.id);
            // Disabled fields are omitted, not represented as a fabricated /0 or protocol 0.
            if (a.value.aclfield.enable) out.attributes[f.name] = decode(f, a);
        }
    }
    return out;
}
void mutablekind(const std::string& k, bool creating) {
    kindcheck(k);
    if (k == "switch" || k == "bridge" || k == "fdb" || (creating && k == "port")) fail(SAI_STATUS_NOT_SUPPORTED, k + " is read-only/existing-only");
}
// Validate every requested value before any SAI operation. ACL table compatibility is
// checked only after this syntax pass, and always before the first mutation.
std::vector<sai_attribute_t> prepare(uint64_t sw, const std::string& kind, const Attrs& input, bool creating, const Key& k) {
    mutablekind(kind, creating);
    if (!creating && input.empty()) invalid("empty update");
    auto fs = fields(kind);
    std::map<std::string, Field> allowed;
    for (auto& f : fs) allowed.emplace(f.name, f);
    std::set<std::string> special;
    if (kind == "neighbor") special = {"router_interface", "ip"};
    if (kind == "route") special = {"virtual_router", "prefix"};
    if (kind == "acl_table") special = {"family"};
    if (kind == "acl_entry") special = {"src", "dst", "protocol"};
    std::vector<sai_attribute_t> attrs;
    for (const auto& kv : input) {
        auto it = allowed.find(kv.first);
        if (it != allowed.end()) {
            if (!creating && !it->second.writable) invalid(kv.first + " is immutable/read-only; replace the object");
            // Port read-only attributes must never be accepted on creation either.
            if (kind == "port" && !it->second.writable) invalid("read-only port attribute: " + kv.first);
            attrs.push_back(encode(it->second, kv.second));
        } else if (special.count(kv.first)) {
            if (!creating && kind != "acl_entry") invalid(kv.first + " is immutable; replace the object");
            if (kv.first == "router_interface" || kv.first == "virtual_router") oid(kv.second);
            else if (kv.first == "ip") ip(kv.second);
            else if (kv.first == "prefix" || kv.first == "src" || kv.first == "dst") prefix(kv.second);
            else if (kv.first == "protocol") number(kv.second, 255);
            else if (kv.first == "family" && kv.second != "ipv4" && kv.second != "ipv6") invalid("family must be ipv4/ipv6");
        } else invalid("unknown attribute for " + kind + ": " + kv.first);
    }
    if (creating) {
        for (auto& f : fs) if (f.required && !input.count(f.name)) invalid("missing required attribute: " + std::string(f.name));
        if (kind == "neighbor" && (!input.count("router_interface") || !input.count("ip"))) invalid("neighbor requires router_interface and ip");
        if (kind == "route" && (!input.count("virtual_router") || !input.count("prefix"))) invalid("route requires virtual_router and prefix");
        if (kind == "acl_table" && !input.count("family")) invalid("acl_table requires family");
        if (kind == "router_interface" && input.count("port") + input.count("vlan") != 1) invalid("router_interface requires exactly one port or vlan");
    }
    auto add32 = [&](sai_attr_id_t id, int32_t v) { sai_attribute_t a{}; a.id = id; a.value.s32 = v; attrs.push_back(a); };
    auto addbool = [&](sai_attr_id_t id, bool v) { sai_attribute_t a{}; a.id = id; a.value.booldata = v; attrs.push_back(a); };
    if (creating) {
        if (kind == "bridge_port") {
            add32(SAI_BRIDGE_PORT_ATTR_TYPE, SAI_BRIDGE_PORT_TYPE_PORT);
            if (!input.count("admin")) addbool(SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, true);
        }
        if (kind == "virtual_router") {
            if (!input.count("ipv4")) addbool(SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V4_STATE, true);
            if (!input.count("ipv6")) addbool(SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V6_STATE, true);
        }
        if (kind == "router_interface") add32(SAI_ROUTER_INTERFACE_ATTR_TYPE, input.count("port") ? SAI_ROUTER_INTERFACE_TYPE_PORT : SAI_ROUTER_INTERFACE_TYPE_VLAN);
        if (kind == "next_hop") add32(SAI_NEXT_HOP_ATTR_TYPE, SAI_NEXT_HOP_TYPE_IP);
        if (kind == "route" && !input.count("action")) add32(SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, SAI_PACKET_ACTION_FORWARD);
        if (kind == "acl_table") {
            bool v4 = input.at("family") == "ipv4";
            addbool(v4 ? SAI_ACL_TABLE_ATTR_FIELD_SRC_IP : SAI_ACL_TABLE_ATTR_FIELD_SRC_IPV6, true);
            addbool(v4 ? SAI_ACL_TABLE_ATTR_FIELD_DST_IP : SAI_ACL_TABLE_ATTR_FIELD_DST_IPV6, true);
            addbool(v4 ? SAI_ACL_TABLE_ATTR_FIELD_IP_PROTOCOL : SAI_ACL_TABLE_ATTR_FIELD_IPV6_NEXT_HEADER, true);
        }
        if (kind == "acl_group") add32(SAI_ACL_TABLE_GROUP_ATTR_TYPE, SAI_ACL_TABLE_GROUP_TYPE_PARALLEL);
        if (kind == "acl_entry" && !input.count("enable")) addbool(SAI_ACL_ENTRY_ATTR_ADMIN_STATE, true);
    }
    if (creating && kind == "bridge_port" && input.count("bridge")) {
        auto default_bridge = read("switch", key(sw, "switch", hex(sw)), SAI_SWITCH_ATTR_DEFAULT_1Q_BRIDGE_ID).value.oid;
        if (oid(input.at("bridge")) != default_bridge)
            fail(SAI_STATUS_NOT_SUPPORTED, "bounded PORT bridge ports belong to default 1Q bridge; other bridge types require a different API");
        attrs.erase(std::remove_if(attrs.begin(), attrs.end(), [](const sai_attribute_t& a) { return a.id == SAI_BRIDGE_PORT_ATTR_BRIDGE_ID; }), attrs.end());
    }
    if (kind == "acl_entry" && (input.count("src") || input.count("dst") || input.count("protocol"))) {
        sai_object_id_t table = creating ? oid(input.at("table")) : read(kind, k, SAI_ACL_ENTRY_ATTR_TABLE_ID).value.oid;
        auto mf = matchfields(tablefamily(key(sw, "acl_table", hex(table))));
        for (const char* name : {"src", "dst", "protocol"}) {
            auto it = input.find(name); if (it == input.end()) continue;
            auto f = std::find_if(mf.begin(), mf.end(), [&](const Field& f) { return std::string(f.name) == name; });
            if (f == mf.end()) fail(SAI_STATUS_NOT_SUPPORTED, std::string("ACL table does not support ") + name);
            attrs.push_back(encode(*f, it->second));
        }
    }
    return attrs;
}
sai_status_t rawcreate(uint64_t sw, const std::string& kind, Key& k, std::vector<sai_attribute_t>& attrs) {
    auto n = static_cast<uint32_t>(attrs.size()); auto a = attrs.data();
    if (kind == "neighbor") { auto p = api<sai_neighbor_api_t>(SAI_API_NEIGHBOR); return p->create_neighbor_entry ? p->create_neighbor_entry(&k.neighbor, n, a) : SAI_STATUS_NOT_SUPPORTED; }
    if (kind == "route") { auto p = api<sai_route_api_t>(SAI_API_ROUTE); return p->create_route_entry ? p->create_route_entry(&k.route, n, a) : SAI_STATUS_NOT_SUPPORTED; }
    auto o = ops(kind); return o.create ? o.create(&k.id, sw, n, a) : SAI_STATUS_NOT_SUPPORTED;
}
sai_status_t rawset(const std::string& kind, const Key& k, const sai_attribute_t& a) {
    if (kind == "neighbor") { auto p = api<sai_neighbor_api_t>(SAI_API_NEIGHBOR); return p->set_neighbor_entry_attribute ? p->set_neighbor_entry_attribute(&k.neighbor, &a) : SAI_STATUS_NOT_SUPPORTED; }
    if (kind == "route") { auto p = api<sai_route_api_t>(SAI_API_ROUTE); return p->set_route_entry_attribute ? p->set_route_entry_attribute(&k.route, &a) : SAI_STATUS_NOT_SUPPORTED; }
    auto o = ops(kind); return o.set ? o.set(k.id, &a) : SAI_STATUS_NOT_SUPPORTED;
}
sai_status_t rawremove(const std::string& kind, const Key& k) {
    if (kind == "neighbor") { auto p = api<sai_neighbor_api_t>(SAI_API_NEIGHBOR); return p->remove_neighbor_entry ? p->remove_neighbor_entry(&k.neighbor) : SAI_STATUS_NOT_SUPPORTED; }
    if (kind == "route") { auto p = api<sai_route_api_t>(SAI_API_ROUTE); return p->remove_route_entry ? p->remove_route_entry(&k.route) : SAI_STATUS_NOT_SUPPORTED; }
    auto o = ops(kind); return o.remove ? o.remove(k.id) : SAI_STATUS_NOT_SUPPORTED;
}
sai_tui::Object readback(uint64_t sw, const std::string& kind, const Key& k, const std::string& op) {
    try { return observe(sw, kind, k); }
    catch (const sai_tui::RpcError& e) { fail(e.status, op + " succeeded for " + kind + " " + k.text + "; READBACK FAILED (mutation not rolled back): " + e.message); }
}
} // namespace

void get(sai_tui::Object& out, uint64_t sw, const std::string& kind, const std::string& text) {
    std::lock_guard<std::mutex> lock(mutex); kindcheck(kind); auto k = key(sw, kind, text); out = observe(sw, kind, k);
}
void create(sai_tui::Object& out, uint64_t sw, const std::string& kind, const Attrs& input) {
    std::lock_guard<std::mutex> lock(mutex);
    Key k; auto attrs = prepare(sw, kind, input, true, k);
    if (kind == "neighbor") k = key(sw, kind, input.at("router_interface") + "@" + input.at("ip"));
    if (kind == "route") k = key(sw, kind, input.at("virtual_router") + "@" + input.at("prefix"));
    // Lists must stay alive until create returns (SAI does not retain caller memory).
    int32_t bind = SAI_ACL_BIND_POINT_TYPE_PORT;
    int32_t action = SAI_ACL_ACTION_TYPE_PACKET_ACTION;
    if (kind == "acl_table" || kind == "acl_group") {
        sai_attribute_t a{}; a.id = kind == "acl_table" ? sai_attr_id_t(SAI_ACL_TABLE_ATTR_ACL_BIND_POINT_TYPE_LIST) : sai_attr_id_t(SAI_ACL_TABLE_GROUP_ATTR_ACL_BIND_POINT_TYPE_LIST);
        a.value.s32list.count = 1; a.value.s32list.list = &bind; attrs.push_back(a);
    }
    if (kind == "acl_table") {
        sai_attribute_t a{}; a.id = SAI_ACL_TABLE_ATTR_ACL_ACTION_TYPE_LIST; a.value.s32list.count = 1; a.value.s32list.list = &action; attrs.push_back(a);
    }
    check(rawcreate(sw, kind, k, attrs), "create " + kind + " failed; no implicit retry");
    if (kind != "route" && kind != "neighbor") k.text = hex(k.id);
    managed[sw].insert({kind, k.text});
    out = readback(sw, kind, k, "create");
}
void set(sai_tui::Object& out, uint64_t sw, const std::string& kind, const std::string& text, const Attrs& input) {
    std::lock_guard<std::mutex> lock(mutex); kindcheck(kind); auto k = key(sw, kind, text);
    auto attrs = prepare(sw, kind, input, false, k);
    size_t applied = 0;
    for (const auto& a : attrs) {
        try { check(rawset(kind, k, a), "SAI set attr " + std::to_string(a.id)); }
        catch (const sai_tui::RpcError& e) {
            std::string detail;
            if (applied) {
                // Earlier writes succeeded: still attempt actual readback, while
                // preserving the original mutation failure as the RPC status.
                try {
                    auto observed = observe(sw, kind, k);
                    detail = "; partial readback observed {";
                    bool first = true;
                    for (const auto& value : observed.attributes) {
                        if (!first) detail += ", ";
                        first = false; detail += value.first + "=" + value.second;
                    }
                    detail += "}";
                } catch (const sai_tui::RpcError& r) {
                    detail = "; PARTIAL READBACK FAILED status " + std::to_string(r.status) + ": " + r.message;
                }
            }
            fail(e.status, "set " + kind + " " + k.text + " failed at SAI attr " + std::to_string(a.id) + " after " + std::to_string(applied) + " successful writes; partial effects possible, no rollback/retry; use tui_get: " + e.message + detail);
        }
        ++applied;
    }
    out = readback(sw, kind, k, "set (" + std::to_string(applied) + " attributes)");
}
void remove(uint64_t sw, const std::string& kind, const std::string& text) {
    std::lock_guard<std::mutex> lock(mutex); mutablekind(kind, false);
    if (kind == "port") fail(SAI_STATUS_NOT_SUPPORTED, "port removal is outside bounded API");
    auto k = key(sw, kind, text);
    check(rawremove(kind, k), "remove " + kind + " " + k.text + " failed; no retry");
    // An actual getter must confirm absence, not an optimistic registry lookup.
    sai_attr_id_t probe = fields(kind).front().id;
    sai_attribute_t a{}; a.id = probe;
    sai_status_t s;
    try { s = rawget(kind, k, &a); }
    catch (const sai_tui::RpcError& e) { fail(e.status, "remove succeeded; absence readback failed for " + kind + " " + k.text + ": " + e.message); }
    if (s == SAI_STATUS_ITEM_NOT_FOUND || s == SAI_STATUS_INVALID_OBJECT_ID) {
        managed[sw].erase({kind, k.text});
        return;
    }
    if (s == SAI_STATUS_SUCCESS) fail(SAI_STATUS_FAILURE, "remove returned success but object still readable: " + kind + " " + k.text);
    fail(s, "remove succeeded; absence could not be confirmed for " + kind + " " + k.text + " (no rollback)");
}
void snapshot(sai_tui::Inventory& out, uint64_t sw) {
    std::lock_guard<std::mutex> lock(mutex); out.objects.clear(); out.warnings.clear();
    out.warnings.push_back("Enumeration is limited to SAI switch ports/default VLAN/default virtual router/default bridge, their members, reachable 1D bridge RIFs, and objects created through this service in this server process; non-default VLAN/L3/ACL objects from other clients or previous processes are not exhaustively discoverable. Default 1Q bridge router ports do not expose individual VLAN RIF OIDs. No persistence.");
    out.warnings.push_back("FDB enumeration is unavailable; use tui_get(fdb, known-key). Notification-derived legacy FDB state is not used as ASIC inventory.");
    std::set<std::pair<std::string, std::string>> seen;
    std::function<void(const std::string&, const std::string&)> add;
    add = [&](const std::string& kind, const std::string& text) {
        if (!seen.insert({kind, text}).second) return;
        try {
            auto k = key(sw, kind, text); out.objects.push_back(observe(sw, kind, k));
            auto attrs = out.objects.back().attributes;
            if (kind == "vlan") for (auto id : list(kind, k, SAI_VLAN_ATTR_MEMBER_LIST)) add("vlan_member", hex(id));
            if (kind == "bridge") for (auto id : list(kind, k, SAI_BRIDGE_ATTR_PORT_LIST)) add("bridge_port", hex(id));
            if (kind == "vlan_member") add("bridge_port", attrs.at("bridge_port"));
            if (kind == "bridge_port" && attrs.count("router_interface") && attrs.at("router_interface") != "0x0") add("router_interface", attrs.at("router_interface"));
        } catch (const sai_tui::RpcError& e) { out.warnings.push_back("get " + kind + " " + text + " failed status " + std::to_string(e.status) + ": " + e.message); }
    };
    add("switch", hex(sw));
    // Discovery must not depend on unrelated switch attributes (e.g. src_mac)
    // being readable. Each default and the port list has its own error boundary.
    auto sk = key(sw, "switch", hex(sw));
    const std::pair<const char*, sai_attr_id_t> defaults[] = {
        {"vlan", SAI_SWITCH_ATTR_DEFAULT_VLAN_ID},
        {"virtual_router", SAI_SWITCH_ATTR_DEFAULT_VIRTUAL_ROUTER_ID},
        {"bridge", SAI_SWITCH_ATTR_DEFAULT_1Q_BRIDGE_ID}};
    for (const auto& d : defaults) {
        try { auto id = read("switch", sk, d.second).value.oid; if (id) add(d.first, hex(id)); }
        catch (const sai_tui::RpcError& e) { out.warnings.push_back("discover default " + std::string(d.first) + " failed status " + std::to_string(e.status) + ": " + e.message); }
    }
    try { for (auto id : list("switch", sk, SAI_SWITCH_ATTR_PORT_LIST)) add("port", hex(id)); }
    catch (const sai_tui::RpcError& e) { out.warnings.push_back("discover ports failed status " + std::to_string(e.status) + ": " + e.message); }
    for (const auto& item : managed[sw]) add(item.first, item.second);
}
void port_counters(std::map<std::string, int64_t>& out, uint64_t, const std::string& text) {
    std::lock_guard<std::mutex> lock(mutex); auto id = oid(text); out.clear();
    auto p = api<sai_port_api_t>(SAI_API_PORT);
    if (!p->get_port_stats) fail(SAI_STATUS_NOT_SUPPORTED, "port stats API unavailable");
    const std::pair<const char*, sai_stat_id_t> stats[] = {
        {"in_octets", SAI_PORT_STAT_IF_IN_OCTETS}, {"out_octets", SAI_PORT_STAT_IF_OUT_OCTETS},
        {"in_packets", SAI_PORT_STAT_IF_IN_UCAST_PKTS}, {"out_packets", SAI_PORT_STAT_IF_OUT_UCAST_PKTS},
        {"in_errors", SAI_PORT_STAT_IF_IN_ERRORS}, {"out_errors", SAI_PORT_STAT_IF_OUT_ERRORS},
        {"in_discards", SAI_PORT_STAT_IF_IN_DISCARDS}, {"out_discards", SAI_PORT_STAT_IF_OUT_DISCARDS}};
    // RPC map has no warning field: omitted keys are the explicit availability signal.
    auto unsupported = [](sai_status_t s) {
        return s == SAI_STATUS_NOT_SUPPORTED || s == SAI_STATUS_NOT_IMPLEMENTED ||
               s == SAI_STATUS_ATTR_NOT_SUPPORTED_0 || s == SAI_STATUS_ATTR_NOT_IMPLEMENTED_0 ||
               s == SAI_STATUS_INVALID_ATTRIBUTE_0;
    };
    for (const auto& stat : stats) {
        uint64_t n = 0; auto statid = stat.second; auto s = p->get_port_stats(id, 1, &statid, &n);
        if (unsupported(s)) continue;
        check(s, std::string("get port counter ") + stat.first);
        if (std::string(stat.first) == "in_packets" || std::string(stat.first) == "out_packets") {
            bool in = stat.first[0] == 'i'; uint64_t m = 0, b = 0;
            sai_stat_id_t mid = in ? SAI_PORT_STAT_IF_IN_MULTICAST_PKTS : SAI_PORT_STAT_IF_OUT_MULTICAST_PKTS;
            sai_stat_id_t bid = in ? SAI_PORT_STAT_IF_IN_BROADCAST_PKTS : SAI_PORT_STAT_IF_OUT_BROADCAST_PKTS;
            auto ms = p->get_port_stats(id, 1, &mid, &m); auto bs = p->get_port_stats(id, 1, &bid, &b);
            // A real failure in either component must not be hidden by an
            // unsupported status on the other component.
            if (!unsupported(ms)) check(ms, "get multicast packet counter");
            if (!unsupported(bs)) check(bs, "get broadcast packet counter");
            if (unsupported(ms) || unsupported(bs)) continue;
            n += m + b;
        }
        int64_t bits; static_assert(sizeof(bits) == sizeof(n), "64-bit thrift counters required"); std::memcpy(&bits, &n, sizeof(bits)); out[stat.first] = bits;
    }
    if (out.empty()) fail(SAI_STATUS_NOT_SUPPORTED, "no bounded port counters supported; all eight keys unavailable");
}
} // namespace tui_rpc
