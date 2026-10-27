// Test-only SAI DSO. Never links or accesses hardware or a vendor SDK.
// Build once normally and once with -DFAKE_SAI_OMIT_LOG_SET to test fail-closed
// symbol resolution. Pass both library runfiles paths to test_sai_dynamic.
extern "C" {
#include <sai.h>
}

#include <atomic>
#include <cstring>
#include <mutex>

namespace {
std::mutex lifecycle;
std::atomic<const sai_service_method_table_t*> host{nullptr};
bool initialized = false;  // Protected by lifecycle.

bool mode(const char* expected) {
    const auto* services = host.load();
    if (!services) return false;
    const char* value = services->profile_get_value(0x1234, "fake.mode");
    return value && std::strcmp(value, expected) == 0;
}

sai_status_t create_switch(sai_object_id_t* id, uint32_t count,
                           const sai_attribute_t* attrs) {
    if (!id || count != 0 || attrs != nullptr) return SAI_STATUS_INVALID_PARAMETER;
    *id = UINT64_C(0xfedcba9876543210);
    return SAI_STATUS_SUCCESS;
}

sai_switch_api_t make_table() {
    sai_switch_api_t table{};
    table.create_switch = &create_switch;
    return table;
}
sai_switch_api_t table = make_table();
}  // namespace

extern "C" sai_status_t sai_api_initialize(
    uint64_t flags, const sai_service_method_table_t* services) {
    if (flags != 0 || !services || !services->profile_get_value ||
        !services->profile_get_next_value) return SAI_STATUS_INVALID_PARAMETER;
    // Invoking exactly the supplied callbacks also checks that the loader did
    // not copy/rewrite the service table or truncate the profile identifier.
    const char* request = services->profile_get_value(0x1234, "fake.initialize");
    if (request && std::strcmp(request, "throw") == 0) throw 42;
    if (request && std::strcmp(request, "fail") == 0) return SAI_STATUS_NO_MEMORY;
    const char* variable = nullptr;
    const char* value = nullptr;
    if (services->profile_get_next_value(0x1234, &variable, &value) != -1)
        return SAI_STATUS_INVALID_PARAMETER;
    std::lock_guard<std::mutex> lock(lifecycle);
    if (initialized) return SAI_STATUS_ITEM_ALREADY_EXISTS;
    host.store(services);
    initialized = true;
    return SAI_STATUS_SUCCESS;
}

extern "C" sai_status_t sai_api_query(sai_api_t api, void** output) {
    if (!output) return SAI_STATUS_INVALID_PARAMETER;
    if (!host.load()) return SAI_STATUS_UNINITIALIZED;
    *output = &table;
    if (api == SAI_API_UNSPECIFIED) throw 42;
    return api == SAI_API_SWITCH ? SAI_STATUS_SUCCESS : SAI_STATUS_NOT_SUPPORTED;
}

extern "C" sai_status_t sai_api_uninitialize(void) {
    if (mode("throw_uninitialize")) throw 42;
    if (mode("fail_uninitialize")) return SAI_STATUS_OBJECT_IN_USE;
    std::lock_guard<std::mutex> lock(lifecycle);
    if (!initialized) return SAI_STATUS_UNINITIALIZED;
    initialized = false;
    host.store(nullptr);
    return SAI_STATUS_SUCCESS;
}

extern "C" sai_status_t sai_query_api_version(sai_api_version_t* version) {
    if (!version) return SAI_STATUS_INVALID_PARAMETER;
    // Deliberately outside the range of both signed 64-bit and unsigned 32-bit.
    *version = UINT64_C(0xfedcba9876543210);
    if (mode("throw_version")) throw 42;
    return mode("fail_version") ? SAI_STATUS_NOT_SUPPORTED : SAI_STATUS_SUCCESS;
}

#ifndef FAKE_SAI_OMIT_LOG_SET
extern "C" sai_status_t sai_log_set(sai_api_t api, sai_log_level_t level) {
    if (api == SAI_API_UNSPECIFIED) throw 42;
    return api == SAI_API_FDB && level == SAI_LOG_LEVEL_NOTICE
               ? SAI_STATUS_TABLE_FULL : SAI_STATUS_INVALID_PARAMETER;
}
#endif
