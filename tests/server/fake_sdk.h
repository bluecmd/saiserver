#pragma once
// Fake SAI SDK (an in-memory object graph) plus packet builders for the
// interface_address responder tests. No SDK library, sockets or hardware.
#include "src/interface_address.h"

#include <array>
#include <condition_variable>
#include <cstdint>
#include <functional>
#include <map>
#include <mutex>
#include <string>
#include <utility>
#include <vector>

namespace fake_sdk {
namespace ia = interface_address;

const sai_object_id_t sw = 1;
const std::array<uint8_t, 6> router{{2,0,0,0,4,1}}, client{{2,3,4,5,6,7}};
extern std::mutex hardware;

using Bytes = std::vector<uint8_t>;
void put16(Bytes& p, size_t off, unsigned n);
unsigned be16(const Bytes& p, size_t off);
// Independent checksum calculation over concatenated pseudo-header and ICMP data.
unsigned checksum(const Bytes& p);
void fix_checksum(Bytes& p);
ia::Target target(const char* ip);
Bytes arp(const ia::Target& t);
Bytes ns(const ia::Target& t, bool dad = false, bool slla = true);
Bytes reply(const ia::Target& t, const Bytes& p);

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
};
extern Fake f;

// SDK entry points backed by f.
sai_status_t query(sai_api_t api, void** out);
sai_status_t keys(sai_object_id_t s, sai_object_type_t type, uint32_t* count, sai_object_key_t* out);
sai_object_type_t object_type(sai_object_id_t id);
sai_object_id_t switch_id(sai_object_id_t id);
sai_status_t enum_values(sai_object_id_t s, sai_object_type_t type, sai_attr_id_t attr, sai_s32_list_t* values);

ia::Sdk sdk();
ia::Options options();
void start(const ia::Options& o = options());
ia::Attributes attrs(unsigned n, const std::string& ip = "192.0.2.1/24");
void error(const std::function<void()>& call, sai_status_t expected = SAI_STATUS_SUCCESS);
void inject(const Bytes& p, sai_object_id_t port, sai_object_id_t trap, sai_object_id_t switch_oid = sw, bool lag = false);
void inject_reliably(const Bytes& p, sai_object_id_t port, sai_object_id_t trap);
void wait_sent(size_t n);
void wait_stat(const std::function<bool(const ia::Status&)>& condition);
}  // namespace fake_sdk
