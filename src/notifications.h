#pragma once
// SDK notification callbacks and the process-wide state they maintain. Kept
// apart from the server main so they can be linked into tests on their own.
#include <atomic>
#include <mutex>
#include <utility>
#include <vector>

extern "C" {
#include <sai.h>
}

// Defined by the RPC listener (or a test), which serves the learned entries.
extern std::vector<std::pair<sai_fdb_entry_t, sai_object_id_t>> gFdbMap;
extern std::mutex gFdbMutex;
extern std::atomic<bool> shutdown_requested;

void on_switch_state_change(sai_object_id_t switch_id,
    sai_switch_oper_status_t switch_oper_status);
void on_fdb_event(uint32_t count, sai_fdb_event_notification_data_t *data);
void on_port_state_change(uint32_t count,
    sai_port_oper_status_notification_t *data);
void on_shutdown_request(sai_object_id_t switch_id);
