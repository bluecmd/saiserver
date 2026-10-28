// Link the real server main against this fake SDK and fake RPC listener. No
// socket is opened. All assertions exercise production CLI/lifecycle ordering.
#include "tests/server/fake_sdk.h"
#include "src/notifications.h"
#include "src/switch_sai_rpc_server.h"
#include "src/tui_rpc.h"
#include <cassert>
#include <cstdlib>
#include <iostream>

using namespace fake_sdk;
std::vector<std::pair<sai_fdb_entry_t, sai_object_id_t>> gFdbMap;
namespace {
bool enabled = false, stopped_rpc = false, created = false;
std::string mode() { const char* p = std::getenv("FAKE_STARTUP_MODE"); return p ? p : "disabled"; }
sai_status_t create_switch(sai_object_id_t* id, uint32_t count, const sai_attribute_t* attrs) {
    assert(count == (enabled ? 7u : 6u));
    bool callback = false;
    for (uint32_t i = 0; i < count; ++i) if (attrs[i].id == SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY) {
        callback = true;
        assert(attrs[i].value.ptr == reinterpret_cast<sai_pointer_t>(ia::packet_callback()));
        f.nodes.at(sw).attrs[attrs[i].id] = attrs[i].value;
    }
    assert(callback == enabled); // Must be installed BEFORE switch creation.
    if (mode() == "bad-callback") f.nodes.at(sw).attrs[SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY].ptr = nullptr;
    *id = sw; created = true; return SAI_STATUS_SUCCESS;
}
sai_status_t set_switch(sai_object_id_t id, const sai_attribute_t* attr) {
    assert(stopped_rpc && !ia::status().running && id == sw);
    assert(attr->id == SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY && !attr->value.ptr);
    if (mode() == "unregister-unsupported") return SAI_STATUS_NOT_SUPPORTED;
    f.nodes.at(id).attrs[attr->id] = attr->value; return SAI_STATUS_SUCCESS;
}
sai_status_t remove_switch(sai_object_id_t id) {
    assert(stopped_rpc && !ia::status().running && id == sw);
    if (mode() == "cleanup-fail" || mode() == "rollback-fail") {
        assert(f.owned() && ia::status().last_status == SAI_STATUS_FAILURE);
        if (mode() == "rollback-fail") assert(f.removes == 2); // Failed rollback was NOT retried.
    } else assert(f.owned() == 0);
    if (mode() == "remove-fail") return SAI_STATUS_FAILURE;
    return SAI_STATUS_SUCCESS;
}
}
extern "C" sai_status_t sai_api_initialize(uint64_t, const sai_service_method_table_t*) {
    enabled = mode() != "disabled";
    f.reset(); f.access(1); f.add(8000, SAI_OBJECT_TYPE_POLICER);
    f.nodes.at(sw).attrs[SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY].ptr = nullptr;
    f.switch_api.create_switch = create_switch; f.switch_api.set_switch_attribute = set_switch;
    f.switch_api.remove_switch = remove_switch;
    if (mode() == "rollback-fail") { f.fail_create = 5; f.fail_remove = 10002; }
    return SAI_STATUS_SUCCESS;
}
extern "C" sai_status_t sai_api_query(sai_api_t api, void** out) { return query(api, out); }
extern "C" sai_status_t sai_query_api_version(sai_api_version_t* version) { *version = 11801; return SAI_STATUS_SUCCESS; }
extern "C" sai_status_t sai_log_set(sai_api_t, sai_log_level_t) { return SAI_STATUS_SUCCESS; }
extern "C" sai_status_t sai_api_uninitialize() {
    assert(created && stopped_rpc && !ia::status().running);
    assert(mode() != "remove-fail");
    if (mode() == "uninit-fail") return SAI_STATUS_FAILURE;
    std::cout << "PASS fake startup/shutdown " << mode() << "\n"; return SAI_STATUS_SUCCESS;
}
extern "C" sai_status_t sai_get_object_key(sai_object_id_t s, sai_object_type_t t, uint32_t* n, sai_object_key_t* out) {
    assert(enabled); return keys(s, t, n, out);
}
extern "C" sai_object_type_t sai_object_type_query(sai_object_id_t id) { assert(enabled); return object_type(id); }
extern "C" sai_object_id_t sai_switch_id_query(sai_object_id_t id) { assert(enabled); return switch_id(id); }
extern "C" sai_status_t sai_query_attribute_enum_values_capability(sai_object_id_t s, sai_object_type_t t, sai_attr_id_t a, sai_s32_list_t* v) {
    assert(enabled); return enum_values(s, t, a, v);
}
extern "C" int start_sai_thrift_rpc_server(int) {
    assert(mode() != "bad-callback" && mode() != "rollback-fail"); // Failure aborts before RPC admission.
    assert(created && ia::status().running == enabled);
    if (mode() == "cleanup-fail") f.fail_remove = ia::status().tables[0];
    shutdown_requested.store(true); // Same shutdown path as SDK shutdown request.
    return 0;
}
extern "C" bool sai_thrift_rpc_server_running() { return true; }
extern "C" void stop_sai_thrift_rpc_server() { stopped_rpc = true; }
