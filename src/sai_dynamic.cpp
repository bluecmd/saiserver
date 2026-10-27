// SDK-neutral entrypoints for the standalone server. Consumers linking their own
// SDK must not link this translation unit. The SDK is a deployment dependency,
// never a build input: set SAI_LIBRARY_PATH to its absolute library filename.
extern "C" {
#include <sai.h>
}

#include <dlfcn.h>
#include <cstdio>
#include <cstdlib>

namespace {
struct Dispatch {
    void* handle = nullptr;
    const char* path = nullptr;
    decltype(&sai_api_initialize) initialize = nullptr;
    decltype(&sai_api_query) query = nullptr;
    decltype(&sai_api_uninitialize) uninitialize = nullptr;
    decltype(&sai_query_api_version) version = nullptr;
    decltype(&sai_log_set) log = nullptr;
};

template <typename Function>
bool resolve(void* handle, const char* path, const char* name,
             Function wrapper, Function& function) noexcept {
    dlerror();
    void* symbol = dlsym(handle, name);
    const char* error = dlerror();
    // POSIX specifies the dlsym conversion to a function pointer. Reject our own
    // wrapper as well, in case a malformed SDK resolves back to this executable.
    function = reinterpret_cast<Function>(symbol);
    if (error || !function || function == wrapper) {
        function = nullptr;
        std::fprintf(stderr,
                     "SAI loader: SAI_LIBRARY_PATH='%s': required symbol %s: %s; "
                     "select a compatible SAI SDK library.\n",
                     path, name, error ? error : "null or recursive entrypoint");
        return false;
    }
    return true;
}

Dispatch load() noexcept try {
    const char* path = std::getenv("SAI_LIBRARY_PATH");
    if (!path || path[0] != '/' || path[1] == '\0') {
        std::fprintf(stderr,
                     "SAI loader: set SAI_LIBRARY_PATH to an absolute SDK shared "
                     "library filename (not a directory or soname); no SDK "
                     "search or fallback is performed.\n");
        return {};
    }
    // RTLD_NOW fails closed on unresolved dependencies; LOCAL avoids exporting
    // vendor symbols into unrelated components of the server.
    void* handle = dlopen(path, RTLD_NOW | RTLD_LOCAL);
    if (!handle) {
        const char* error = dlerror();
        std::fprintf(stderr,
                     "SAI loader: cannot open SAI_LIBRARY_PATH='%s': %s; check "
                     "the SDK filename and its runtime dependencies.\n",
                     path, error ? error : "dlopen failed");
        return {};
    }

    // Intentionally pin even an incompatible library for process lifetime.
    // No dlclose, including at static destruction or sai_api_uninitialize:
    // vendor threads, callbacks and previously returned tables must never point
    // into unmapped code. Publish nothing unless ALL required symbols exist.
    Dispatch result;
    if (!resolve(handle, path, "sai_api_initialize", &sai_api_initialize, result.initialize) ||
        !resolve(handle, path, "sai_api_query", &sai_api_query, result.query) ||
        !resolve(handle, path, "sai_api_uninitialize", &sai_api_uninitialize, result.uninitialize) ||
        !resolve(handle, path, "sai_query_api_version", &sai_query_api_version, result.version) ||
        !resolve(handle, path, "sai_log_set", &sai_log_set, result.log)) {
        return {};
    }
    result.handle = handle;
    // getenv storage may change later. Diagnostics need no cached environment
    // pointer; optional resolution uses this pinned handle, never a new dlopen.
    result.path = "<already loaded SDK>";
    return result;
} catch (...) {
    // A C++ DSO constructor may throw during dlopen. Cache that failure too,
    // rather than letting static initialization retry or an exception escape.
    std::fprintf(stderr, "SAI loader: exception while loading SAI_LIBRARY_PATH; "
                         "check the selected SDK and restart the process.\n");
    return {};
}

const Dispatch& dispatch() {
    // C++11 static initialization synchronizes concurrent first callers. Both
    // success and failure are sticky: configure the environment BEFORE any SAI
    // call, and restart the process to change SDKs or retry a failed load.
    static const Dispatch instance = load();
    return instance;
}

struct Optional {
    decltype(&sai_get_object_key) keys = nullptr;
    decltype(&sai_object_type_query) type = nullptr;
    decltype(&sai_switch_id_query) switch_id = nullptr;
    decltype(&sai_query_attribute_enum_values_capability) enums = nullptr;
};
const Optional& optional() {
    // Lazy, sticky and from the SAME SDK: disabled servers need no new symbols.
    static const Optional value = [] {
        Optional o;
        const auto& d = dispatch();
        if (!d.handle) return o;
        resolve(d.handle, d.path, "sai_get_object_key", &sai_get_object_key, o.keys);
        resolve(d.handle, d.path, "sai_object_type_query", &sai_object_type_query, o.type);
        resolve(d.handle, d.path, "sai_switch_id_query", &sai_switch_id_query, o.switch_id);
        resolve(d.handle, d.path, "sai_query_attribute_enum_values_capability", &sai_query_attribute_enum_values_capability, o.enums);
        return o;
    }();
    return value;
}

template <typename Call>
sai_status_t guarded(const char* entrypoint, Call call) noexcept {
    try {
        return call(dispatch());
    } catch (...) {
        // Also contain exceptions from a C++ SDK or a host callback. The C ABI
        // must never propagate one. SDK status codes otherwise pass unchanged.
        std::fprintf(stderr, "SAI loader: exception in %s; returning SAI_STATUS_FAILURE.\n",
                     entrypoint);
        return SAI_STATUS_FAILURE;
    }
}
}  // namespace

// SDK lifecycle semantics are deliberately not emulated: each initialize and
// uninitialize is forwarded, including vendor duplicate-initialization errors.
// As with direct SDK linking, callers must coordinate SDK lifecycle/table use.
extern "C" sai_status_t sai_api_initialize(
    uint64_t flags, const sai_service_method_table_t* services) {
    return guarded("sai_api_initialize", [=](const Dispatch& sdk) {
        return sdk.initialize ? sdk.initialize(flags, services) : SAI_STATUS_FAILURE;
    });
}

extern "C" sai_status_t sai_api_query(sai_api_t api, void** api_method_table) {
    if (!api_method_table) return SAI_STATUS_INVALID_PARAMETER;
    *api_method_table = nullptr;
    const sai_status_t status = guarded("sai_api_query", [=](const Dispatch& sdk) {
        return sdk.query ? sdk.query(api, api_method_table) : SAI_STATUS_FAILURE;
    });
    if (status != SAI_STATUS_SUCCESS) *api_method_table = nullptr;
    return status;
}

extern "C" sai_status_t sai_api_uninitialize(void) {
    return guarded("sai_api_uninitialize", [](const Dispatch& sdk) {
        return sdk.uninitialize ? sdk.uninitialize() : SAI_STATUS_FAILURE;
    });
}

extern "C" sai_status_t sai_query_api_version(sai_api_version_t* version) {
    if (!version) return SAI_STATUS_INVALID_PARAMETER;
    *version = 0;
    const sai_status_t status = guarded("sai_query_api_version", [=](const Dispatch& sdk) {
        return sdk.version ? sdk.version(version) : SAI_STATUS_FAILURE;
    });
    if (status != SAI_STATUS_SUCCESS) *version = 0;
    return status;
}

extern "C" sai_status_t sai_log_set(sai_api_t api, sai_log_level_t log_level) {
    return guarded("sai_log_set", [=](const Dispatch& sdk) {
        return sdk.log ? sdk.log(api, log_level) : SAI_STATUS_FAILURE;
    });
}

extern "C" sai_status_t sai_get_object_key(sai_object_id_t sw, sai_object_type_t type,
                                           uint32_t* count, sai_object_key_t* keys) {
    if (!count || (*count && !keys)) return SAI_STATUS_INVALID_PARAMETER;
    return guarded("sai_get_object_key", [=](const Dispatch&) {
        auto f = optional().keys;
        return f ? f(sw, type, count, keys) : SAI_STATUS_NOT_SUPPORTED;
    });
}
extern "C" sai_status_t sai_query_attribute_enum_values_capability(
    sai_object_id_t sw, sai_object_type_t type, sai_attr_id_t attr, sai_s32_list_t* values) {
    if (!values || (values->count && !values->list)) return SAI_STATUS_INVALID_PARAMETER;
    return guarded("sai_query_attribute_enum_values_capability", [=](const Dispatch&) {
        auto f = optional().enums;
        return f ? f(sw, type, attr, values) : SAI_STATUS_NOT_SUPPORTED;
    });
}
extern "C" sai_object_type_t sai_object_type_query(sai_object_id_t id) {
    try { auto f = optional().type; return f ? f(id) : SAI_OBJECT_TYPE_NULL; }
    catch (...) { std::fprintf(stderr, "SAI loader: exception in sai_object_type_query\n"); return SAI_OBJECT_TYPE_NULL; }
}
extern "C" sai_object_id_t sai_switch_id_query(sai_object_id_t id) {
    try { auto f = optional().switch_id; return f ? f(id) : SAI_NULL_OBJECT_ID; }
    catch (...) { std::fprintf(stderr, "SAI loader: exception in sai_switch_id_query\n"); return SAI_NULL_OBJECT_ID; }
}
