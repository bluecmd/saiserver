// Standalone, hardware-free loader tests (no testing framework needed).
// Usage: test_sai_dynamic <complete-fake-DSO> <incomplete-fake-DSO> [optional-symbol-fake-DSO]
// The second DSO uses tests/fake_sai.cpp with -DFAKE_SAI_OMIT_LOG_SET.
// Arguments are rlocation paths, resolved here; the loader itself accepts ONLY
// an absolute filename. No test discovers or loads an installed/vendor SDK.
extern "C" {
#include <sai.h>
}

#include <sys/wait.h>
#include <unistd.h>
#include <atomic>
#include <cerrno>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <functional>
#include <memory>
#include <string>
#include <thread>
#include <vector>

#include "rules_cc/cc/runfiles/runfiles.h"

#define CHECK(condition) do { if (!(condition)) { \
    std::fprintf(stderr, "%s:%d: check failed: %s\n", __FILE__, __LINE__, #condition); \
    std::exit(1); \
} } while (false)

namespace {
constexpr sai_api_version_t kVersion = UINT64_C(0xfedcba9876543210);
std::atomic<const char*> request{"ok"};
std::atomic<int> initialize_calls{0};
std::atomic<int> next_calls{0};

const char* get_value(sai_switch_profile_id_t profile, const char* key) {
    CHECK(profile == 0x1234);
    CHECK(key != nullptr);
    if (std::strcmp(key, "fake.initialize") == 0) ++initialize_calls;
    else CHECK(std::strcmp(key, "fake.mode") == 0);
    return request.load();
}
int get_next(sai_switch_profile_id_t profile, const char** variable, const char** value) {
    CHECK(profile == 0x1234 && variable && value);
    ++next_calls;
    return -1;
}
const sai_service_method_table_t services = {&get_value, &get_next};

void select(const std::string& path) {
    CHECK(setenv("SAI_LIBRARY_PATH", path.c_str(), 1) == 0);
}

void check_unavailable() {
    sai_api_version_t version = kVersion;
    void* table = reinterpret_cast<void*>(1);
    CHECK(sai_query_api_version(&version) == SAI_STATUS_FAILURE);
    CHECK(version == 0);
    CHECK(sai_api_initialize(0, &services) == SAI_STATUS_FAILURE);
    CHECK(sai_api_query(SAI_API_SWITCH, &table) == SAI_STATUS_FAILURE);
    CHECK(table == nullptr);
    CHECK(sai_log_set(SAI_API_FDB, SAI_LOG_LEVEL_NOTICE) == SAI_STATUS_FAILURE);
    CHECK(sai_api_uninitialize() == SAI_STATUS_FAILURE);
    CHECK(initialize_calls == 0);  // Incomplete libraries must publish nothing.
}

// Each case gets a fresh process: the production loader intentionally caches
// first-load failure as well as success, and offers no test-only reset hook.
void run_case(const char* name, const std::function<void()>& body,
              const std::string& expected_diagnostic = "") {
    int pipefd[2];
    CHECK(pipe(pipefd) == 0);
    const pid_t pid = fork();
    CHECK(pid >= 0);
    if (pid == 0) {
        close(pipefd[0]);
        CHECK(dup2(pipefd[1], STDERR_FILENO) >= 0);
        close(pipefd[1]);
        body();
        _exit(0);
    }
    close(pipefd[1]);
    std::string diagnostics;
    char buffer[1024];
    for (;;) {
        const ssize_t n = read(pipefd[0], buffer, sizeof(buffer));
        if (n > 0) diagnostics.append(buffer, static_cast<size_t>(n));
        else if (n == 0) break;
        else CHECK(errno == EINTR);
    }
    close(pipefd[0]);
    int status = 0;
    CHECK(waitpid(pid, &status, 0) == pid);
    if (!WIFEXITED(status) || WEXITSTATUS(status) != 0 ||
        (!expected_diagnostic.empty() && diagnostics.find(expected_diagnostic) == std::string::npos)) {
        std::fprintf(stderr, "FAIL %s (wait status %d):\n%s", name, status, diagnostics.c_str());
        std::exit(1);
    }
    std::printf("PASS %s\n", name);
}

std::string absolute_runfile(const char* rlocationpath) {
    using rules_cc::cc::runfiles::Runfiles;
    static const std::unique_ptr<Runfiles> runfiles(Runfiles::CreateForTest(BAZEL_CURRENT_REPOSITORY));
    CHECK(runfiles != nullptr);
    char* absolute = realpath(runfiles->Rlocation(rlocationpath).c_str(), nullptr);
    CHECK(absolute != nullptr);
    std::string result(absolute);
    std::free(absolute);
    return result;
}
}  // namespace

int main(int argc, char** argv) {
    if (argc != 3 && argc != 4) {
        std::fprintf(stderr, "Usage: %s <complete-fake-DSO> <fake-DSO-built-with-FAKE_SAI_OMIT_LOG_SET> [optional-symbol-fake-DSO]\n", argv[0]);
        return 2;
    }
    const std::string complete = absolute_runfile(argv[1]);
    const std::string incomplete = absolute_runfile(argv[2]);
    CHECK(complete != incomplete);
    // Override any deployment SAI_LIBRARY_PATH before any loader call.
    CHECK(unsetenv("SAI_LIBRARY_PATH") == 0);
    const char* tmp = std::getenv("TEST_TMPDIR");
    std::string pattern = std::string(tmp ? tmp : "/tmp") + "/sai-dynamic-XXXXXX";
    std::vector<char> writable(pattern.begin(), pattern.end());
    writable.push_back('\0');
    CHECK(mkdtemp(writable.data()) != nullptr);
    const std::string directory = absolute_runfile(writable.data());
    const std::string missing = directory + "/missing.so";
    const std::string invalid = directory + "/invalid.so";
    FILE* file = std::fopen(invalid.c_str(), "w");
    CHECK(file != nullptr);
    CHECK(std::fputs("not an ELF library\n", file) >= 0);
    CHECK(std::fclose(file) == 0);

    run_case("unset SDK, sticky failure", [&] {
        check_unavailable();
        select(complete);
        check_unavailable();
    }, "set SAI_LIBRARY_PATH to an absolute SDK shared library filename");
    run_case("empty SDK", [&] { select(""); check_unavailable(); }, "SAI_LIBRARY_PATH");
    run_case("bare soname is forbidden", [&] { select("libsai.so"); check_unavailable(); }, "no SDK search");
    run_case("relative filename is forbidden", [&] { select("./libsai.so"); check_unavailable(); }, "absolute");
    run_case("root is not a filename", [&] { select("/"); check_unavailable(); }, "filename");
    run_case("absent SDK", [&] { select(missing); check_unavailable(); }, missing);
    run_case("invalid SDK", [&] { select(invalid); check_unavailable(); }, "cannot open SAI_LIBRARY_PATH");
    run_case("directory is not an SDK", [&] { select(directory); check_unavailable(); }, directory);
    run_case("missing required symbol, no partial dispatch", [&] {
        select(incomplete);
        check_unavailable();
        select(complete);
        check_unavailable();
    }, "required symbol sai_log_set");

    run_case("forwarding, unsigned version, errors, pinned tables", [&] {
        select(complete);
        sai_api_version_t version = 0;
        CHECK(sai_query_api_version(nullptr) == SAI_STATUS_INVALID_PARAMETER);
        CHECK(sai_api_query(SAI_API_SWITCH, nullptr) == SAI_STATUS_INVALID_PARAMETER);
        CHECK(sai_query_api_version(&version) == SAI_STATUS_SUCCESS && version == kVersion);
        CHECK(sai_api_initialize(UINT64_C(1) << 63, &services) == SAI_STATUS_INVALID_PARAMETER);
        CHECK(sai_api_initialize(0, nullptr) == SAI_STATUS_INVALID_PARAMETER);
        request = "fail";
        CHECK(sai_api_initialize(0, &services) == SAI_STATUS_NO_MEMORY);
        request = "ok";
        CHECK(sai_api_initialize(0, &services) == SAI_STATUS_SUCCESS);
        CHECK(sai_api_initialize(0, &services) == SAI_STATUS_ITEM_ALREADY_EXISTS);
        CHECK(initialize_calls == 3 && next_calls == 2);
        void* raw = nullptr;
        CHECK(sai_api_query(SAI_API_SWITCH, &raw) == SAI_STATUS_SUCCESS && raw);
        auto* table = static_cast<sai_switch_api_t*>(raw);
        sai_object_id_t id = 0;
        CHECK(table->create_switch(&id, 0, nullptr) == SAI_STATUS_SUCCESS && id == kVersion);
        CHECK(sai_log_set(SAI_API_FDB, SAI_LOG_LEVEL_NOTICE) == SAI_STATUS_TABLE_FULL);
        CHECK(sai_log_set(SAI_API_SWITCH, SAI_LOG_LEVEL_ERROR) == SAI_STATUS_INVALID_PARAMETER);
        CHECK(sai_api_query(SAI_API_PORT, &raw) == SAI_STATUS_NOT_SUPPORTED && !raw);
        request = "fail_version";
        CHECK(sai_query_api_version(&version) == SAI_STATUS_NOT_SUPPORTED && version == 0);
        request = "fail_uninitialize";
        CHECK(sai_api_uninitialize() == SAI_STATUS_OBJECT_IN_USE);
        request = "ok";
        CHECK(sai_api_uninitialize() == SAI_STATUS_SUCCESS);
        CHECK(sai_api_uninitialize() == SAI_STATUS_UNINITIALIZED);
        // Changing the environment cannot replace/unmap an already loaded SDK.
        select(missing);
        CHECK(sai_query_api_version(&version) == SAI_STATUS_SUCCESS && version == kVersion);
        CHECK(sai_api_initialize(0, &services) == SAI_STATUS_SUCCESS);
        CHECK(sai_api_query(SAI_API_SWITCH, &raw) == SAI_STATUS_SUCCESS && raw == table);
        CHECK(table->create_switch(&id, 0, nullptr) == SAI_STATUS_SUCCESS);
        CHECK(sai_api_uninitialize() == SAI_STATUS_SUCCESS);
    });

    run_case("exceptions never escape the C ABI", [&] {
        select(complete);
        request = "throw";
        CHECK(sai_api_initialize(0, &services) == SAI_STATUS_FAILURE);
        request = "ok";
        CHECK(sai_api_initialize(0, &services) == SAI_STATUS_SUCCESS);
        void* raw = reinterpret_cast<void*>(1);
        CHECK(sai_api_query(SAI_API_UNSPECIFIED, &raw) == SAI_STATUS_FAILURE && !raw);
        CHECK(sai_log_set(SAI_API_UNSPECIFIED, SAI_LOG_LEVEL_NOTICE) == SAI_STATUS_FAILURE);
        request = "throw_version";
        sai_api_version_t version = kVersion;
        CHECK(sai_query_api_version(&version) == SAI_STATUS_FAILURE && version == 0);
        request = "throw_uninitialize";
        CHECK(sai_api_uninitialize() == SAI_STATUS_FAILURE);
        request = "ok";
        CHECK(sai_api_uninitialize() == SAI_STATUS_SUCCESS);
    }, "exception in sai_api_initialize");

    run_case("concurrent first load and SDK forwarding", [&] {
        select(complete);
        constexpr int count = 24;
        std::atomic<int> ready{0};
        std::atomic<bool> start{false};
        std::atomic<int> successes{0};
        std::vector<std::thread> threads;
        for (int i = 0; i < count; ++i) {
            threads.emplace_back([&] {
                ++ready;
                while (!start.load()) std::this_thread::yield();
                sai_api_version_t version = 0;
                CHECK(sai_query_api_version(&version) == SAI_STATUS_SUCCESS && version == kVersion);
                const sai_status_t status = sai_api_initialize(0, &services);
                if (status == SAI_STATUS_SUCCESS) ++successes;
                else CHECK(status == SAI_STATUS_ITEM_ALREADY_EXISTS);
                for (int n = 0; n < 50; ++n) {
                    void* table = nullptr;
                    CHECK(sai_api_query(SAI_API_SWITCH, &table) == SAI_STATUS_SUCCESS && table);
                    CHECK(sai_log_set(SAI_API_FDB, SAI_LOG_LEVEL_NOTICE) == SAI_STATUS_TABLE_FULL);
                }
            });
        }
        while (ready.load() != count) std::this_thread::yield();
        start = true;
        for (auto& thread : threads) thread.join();
        CHECK(successes == 1 && initialize_calls == count && next_calls == count);
        CHECK(sai_api_uninitialize() == SAI_STATUS_SUCCESS);
    });

    run_case("optional symbols absent do not poison required dispatch", [&] {
        select(complete);
        uint32_t count = 0; sai_s32_list_t values{};
        CHECK(sai_get_object_key(kVersion, SAI_OBJECT_TYPE_HOSTIF_TRAP, &count, nullptr) == SAI_STATUS_NOT_SUPPORTED);
        CHECK(sai_query_attribute_enum_values_capability(kVersion, SAI_OBJECT_TYPE_HOSTIF_PACKET,
              SAI_HOSTIF_PACKET_ATTR_HOSTIF_TX_TYPE, &values) == SAI_STATUS_NOT_SUPPORTED);
        CHECK(sai_object_type_query(kVersion) == SAI_OBJECT_TYPE_NULL);
        CHECK(sai_switch_id_query(kVersion) == SAI_NULL_OBJECT_ID);
        sai_api_version_t version = 0;
        CHECK(sai_query_api_version(&version) == SAI_STATUS_SUCCESS && version == kVersion);
    }, "sai_get_object_key");
    if (argc == 4) {
        const std::string optional = absolute_runfile(argv[3]);
        run_case("optional forwarding, buffers, identity, exceptions and pinned SDK", [&] {
            select(optional);
            uint32_t count = 0; sai_object_key_t key{};
            CHECK(sai_get_object_key(kVersion, SAI_OBJECT_TYPE_HOSTIF_TRAP, &count, nullptr) == SAI_STATUS_BUFFER_OVERFLOW && count == 1);
            CHECK(sai_get_object_key(kVersion, SAI_OBJECT_TYPE_HOSTIF_TRAP, &count, &key) == SAI_STATUS_SUCCESS);
            CHECK(key.key.object_id == kVersion + 1);
            CHECK(sai_object_type_query(key.key.object_id) == SAI_OBJECT_TYPE_HOSTIF_TRAP);
            CHECK(sai_switch_id_query(key.key.object_id) == kVersion);
            sai_s32_list_t values{}; int32_t value = -1;
            CHECK(sai_query_attribute_enum_values_capability(kVersion, SAI_OBJECT_TYPE_HOSTIF_PACKET,
                  SAI_HOSTIF_PACKET_ATTR_HOSTIF_TX_TYPE, &values) == SAI_STATUS_BUFFER_OVERFLOW && values.count == 1);
            values.list = &value;
            CHECK(sai_query_attribute_enum_values_capability(kVersion, SAI_OBJECT_TYPE_HOSTIF_PACKET,
                  SAI_HOSTIF_PACKET_ATTR_HOSTIF_TX_TYPE, &values) == SAI_STATUS_SUCCESS && value == SAI_HOSTIF_TX_TYPE_PIPELINE_BYPASS);
            CHECK(sai_get_object_key(42, SAI_OBJECT_TYPE_HOSTIF_TRAP, &count, &key) == SAI_STATUS_FAILURE);
            CHECK(sai_object_type_query(42) == SAI_OBJECT_TYPE_NULL && sai_switch_id_query(42) == SAI_NULL_OBJECT_ID);
            CHECK(sai_query_attribute_enum_values_capability(42, SAI_OBJECT_TYPE_HOSTIF_PACKET,
                  SAI_HOSTIF_PACKET_ATTR_HOSTIF_TX_TYPE, &values) == SAI_STATUS_FAILURE);
            CHECK(sai_get_object_key(kVersion, SAI_OBJECT_TYPE_HOSTIF_TRAP, nullptr, nullptr) == SAI_STATUS_INVALID_PARAMETER);
            CHECK(sai_query_attribute_enum_values_capability(kVersion, SAI_OBJECT_TYPE_HOSTIF_PACKET, 0, nullptr) == SAI_STATUS_INVALID_PARAMETER);
            select(complete); // Never resolve against a different library after env changes.
            CHECK(sai_switch_id_query(kVersion + 1) == kVersion);
        });
    }

    CHECK(unlink(invalid.c_str()) == 0);
    CHECK(rmdir(directory.c_str()) == 0);
    return 0;
}
