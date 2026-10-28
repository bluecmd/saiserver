// Link the actual server implementation without starting it or initializing SAI.
extern "C" {
#include <sai.h>
}
#include "src/switch_sai_rpc_server.h"
#include <sai_tui_types.h>
#include <switch_sai_rpc.h>
#include <mutex>

// The legacy server library uses application-owned switch/callback state.
sai_object_id_t gSwitchId = SAI_NULL_OBJECT_ID;
std::mutex gFdbMutex;

// The SAI C API comes from @saiserver//:sai_loader, as in a real deployment.
// It loads nothing until SAI_LIBRARY_PATH is used; no ASIC APIs are invoked.

int main() {
    // A volatile reference forces real library linkage, not a header-only check.
    auto volatile entrypoint = &start_sai_thrift_rpc_server;
    sai_tui::Inventory inventory;
    inventory.warnings.push_back("downstream-link-smoke");
    return entrypoint && inventory.warnings.front() == "downstream-link-smoke" ? 0 : 1;
}
