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
