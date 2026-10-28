// Reuse the packet/topology fake, not a mock responder. No sockets or SDK DSO.
#include "fake_sdk.h"
#include "tui_rpc.h"
#include "bounded_rpc_processor.h"
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/transport/TBufferTransports.h>
#include <cassert>
#include <iostream>

using namespace fake_sdk;

extern "C" sai_status_t sai_api_query(sai_api_t api, void** out) { return query(api, out); }
unsigned uninitializes = 0, switch_removes = 0, callback_sets = 0;
extern "C" sai_status_t sai_api_uninitialize() { ++uninitializes; return SAI_STATUS_SUCCESS; }
namespace {
sai_status_t set_switch(sai_object_id_t id, const sai_attribute_t* attr) {
    assert(id == sw && attr->id == SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY);
    ++callback_sets; f.nodes.at(id).attrs[attr->id] = attr->value; return SAI_STATUS_SUCCESS;
}
sai_status_t remove_switch(sai_object_id_t id) {
    assert(id == sw && !ia::status().running); // Only used after worker joined.
    ++switch_removes; return SAI_STATUS_SUCCESS;
}
void switch_observation() {
    f.oid(sw, SAI_SWITCH_ATTR_DEFAULT_VLAN_ID, 0);
    f.oid(sw, SAI_SWITCH_ATTR_DEFAULT_VIRTUAL_ROUTER_ID, 0);
    f.oid(sw, SAI_SWITCH_ATTR_DEFAULT_1Q_BRIDGE_ID, 0);
    std::copy(router.begin(), router.end(), f.nodes.at(sw).attrs[SAI_SWITCH_ATTR_SRC_MAC_ADDRESS].mac);
}
void rpc_error(const std::function<void()>& call, sai_status_t status) {
    try { call(); assert(false); } catch (const sai_tui::RpcError& e) { assert(e.status == status); }
}
void advertised(const char* expected, const char* preset) {
    sai_tui::Inventory inventory; tui_rpc::snapshot(inventory, sw);
    bool found = false;
    for (const auto& obj : inventory.objects) if (obj.kind == "switch") {
        found = true; assert(obj.attributes.at("interface_address_backend") == expected);
        assert(obj.attributes.at("preset_api") == preset);
    }
    assert(found);
}
struct Handler : switch_sai::switch_sai_rpcNull {
    unsigned legacy = 0;
    switch_sai::sai_thrift_status_t sai_thrift_clear_port_all_stats(const int64_t) override { ++legacy; return 0; }
    void tui_get(sai_tui::Object& out, const std::string& kind, const std::string& key) override { tui_rpc::get(out, sw, kind, key); }
};
void gate_test(bool allowed) {
    using apache::thrift::transport::TMemoryBuffer;
    using apache::thrift::protocol::TBinaryProtocol;
    auto req = std::make_shared<TMemoryBuffer>(), res = std::make_shared<TMemoryBuffer>();
    auto in = std::make_shared<TBinaryProtocol>(req), out = std::make_shared<TBinaryProtocol>(res);
    auto handler = std::make_shared<Handler>(); std::atomic<bool> accepting{true};
    BoundedRpcProcessor processor(handler, accepting);
    switch_sai::switch_sai_rpcClient client(out, in);
    client.send_sai_thrift_clear_port_all_stats(201); assert(processor.process(in, out, nullptr));
    bool rejected = false;
    try { client.recv_sai_thrift_clear_port_all_stats(); }
    catch (const apache::thrift::TApplicationException&) { rejected = true; }
    assert(rejected == !allowed && handler->legacy == unsigned(allowed));
    sai_tui::Object observed;
    client.send_tui_get("switch", "1"); assert(processor.process(in, out, nullptr)); client.recv_tui_get(observed);
    accepting.store(false);
    client.send_tui_get("switch", "1"); assert(processor.process(in, out, nullptr));
    try { client.recv_tui_get(observed); assert(false); } catch (const apache::thrift::TApplicationException&) {}
}
}
int main() {
    f.reset(); f.access(1); switch_observation();
    assert(!tui_rpc::bounded_only()); advertised("disabled", "0"); gate_test(true);
    sai_tui::Object out;
    rpc_error([&] { tui_rpc::create(out, sw, "interface_address", attrs(1)); }, SAI_STATUS_NOT_SUPPORTED);
    auto no_v6 = options(); no_v6.static_ipv6_no_dad = false;
    tui_rpc::start_interface_addresses(sw, no_v6, sdk()); advertised("disabled", "0");
    rpc_error([&] { tui_rpc::create(out, sw, "interface_address", attrs(1, "2001:db8::1/64")); }, SAI_STATUS_NOT_SUPPORTED);
    tui_rpc::stop_interface_addresses();
    tui_rpc::start_interface_addresses(sw, options(), sdk()); advertised("enabled", "1"); gate_test(false);
    tui_rpc::create(out, sw, "interface_address", attrs(1)); const auto key = out.key;
    assert(key == "0x3e9@192.0.2.1/24" && out.attributes.at("observation_source") == "software-responder");
    tui_rpc::get(out, sw, "interface_address", "1001@192.0.2.1/24"); assert(out.key == key);
    auto extra = attrs(1); extra["vr"] = "2";
    rpc_error([&] { tui_rpc::create(out, sw, "interface_address", extra); }, SAI_STATUS_INVALID_PARAMETER);
    rpc_error([&] { tui_rpc::set(out, sw, "interface_address", key, attrs(1)); }, SAI_STATUS_NOT_SUPPORTED);
    rpc_error([&] { tui_rpc::set(out, sw, "port", "201", {{"pvid", "102"}}); }, SAI_STATUS_OBJECT_IN_USE);
    rpc_error([&] { tui_rpc::remove(sw, "router_interface", "1001"); }, SAI_STATUS_OBJECT_IN_USE);
    rpc_error([&] { tui_rpc::create(out, sw, "vlan", {{"vlan_id", "55"}}); }, SAI_STATUS_OBJECT_IN_USE);
    tui_rpc::create(out, sw, "interface_address", attrs(1, "2001:0db8::1234/64"));
    const auto v6key = out.key; assert(v6key == "0x3e9@2001:db8::1234/64");
    sai_tui::Inventory inventory; tui_rpc::snapshot(inventory, sw);
    unsigned addresses = 0; for (const auto& obj : inventory.objects) if (obj.kind == "interface_address") ++addresses;
    assert(addresses == 2); // list must run outside shared SAI lock (no self-deadlock).
    const auto state = ia::status();
    inject_reliably(arp(target("192.0.2.1")), 201, state.traps[0]); wait_sent(1);
    inject_reliably(ns(target("2001:db8::1234")), 201, state.traps[1]); wait_sent(2);
    assert(be16(f.sent[0].second, 20) == 2 && f.sent[1].second[54] == 136);
    tui_rpc::remove(sw, "interface_address", key);
    rpc_error([&] { tui_rpc::get(out, sw, "interface_address", key); }, SAI_STATUS_ITEM_NOT_FOUND);
    tui_rpc::remove(sw, "interface_address", v6key);
    // A live TX faults the service; inventory must stop advertising enabled.
    tui_rpc::create(out, sw, "interface_address", attrs(1));
    f.send_error = true; inject_reliably(arp(target("192.0.2.1")), 201, state.traps[0]);
    wait_stat([](const ia::Status& s) { return !s.running; }); advertised("failed", "0"); gate_test(false);
    rpc_error([&] { tui_rpc::get(out, sw, "interface_address", key); }, SAI_STATUS_NOT_SUPPORTED);
    // Cleanup failures retain status and owned dependencies; only an explicit
    // second stop is retried. Callback is harmless after joined stop failure.
    f.fail_remove = state.tables[0];
    error([] { tui_rpc::stop_interface_addresses(); }, SAI_STATUS_FAILURE);
    assert(ia::status().tables[0] == f.fail_remove && ia::status().last_status == SAI_STATUS_FAILURE);
    inject(arp(target("192.0.2.1")), 201, state.traps[0]);
    f.fail_remove = 0; tui_rpc::stop_interface_addresses(); assert(f.owned() == 0);
    f.switch_api.set_switch_attribute = set_switch; f.switch_api.remove_switch = remove_switch;
    assert(tui_rpc::shutdown_switch(sw) == SAI_STATUS_SUCCESS);
    assert(callback_sets == 1 && switch_removes == 1 && uninitializes == 1);
    // A replacement callback must never be cleared.
    f.nodes.at(sw).attrs[SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY].ptr = reinterpret_cast<void*>(1);
    assert(tui_rpc::shutdown_switch(sw) == SAI_STATUS_SUCCESS && callback_sets == 1);
    std::cout << "interface_address RPC: CRUD/snapshot/ARP/ND/gating/fault/cleanup integration passed\n";
}
