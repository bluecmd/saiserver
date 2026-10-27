// Link the actual server implementation without starting it or initializing SAI.
extern "C" {
#include <sai.h>
}
#include <switch_sai_rpc_server.h>
#include <sai_tui_types.h>
#include <switch_sai_rpc.h>
#include <mutex>

// The legacy server library uses application-owned switch/callback state.
sai_object_id_t gSwitchId = SAI_NULL_OBJECT_ID;
std::mutex gFdbMutex;

// Test-only C API provider: the embedding application normally links a pinned
// SDK cc_import, or //src:sai_dynamic. No ASIC APIs are invoked by this test.
extern "C" sai_status_t sai_api_query(sai_api_t, void** output) {
    if (output) *output = nullptr;
    return SAI_STATUS_NOT_SUPPORTED;
}

int main() {
    // A volatile reference forces real library linkage, not a header-only check.
    auto volatile entrypoint = &start_sai_thrift_rpc_server;
    sai_tui::Inventory inventory;
    inventory.warnings.push_back("downstream-link-smoke");
    return entrypoint && inventory.warnings.front() == "downstream-link-smoke" ? 0 : 1;
}
