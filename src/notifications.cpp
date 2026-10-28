#include "src/notifications.h"

#include <algorithm>
#include <cstring>

std::mutex gFdbMutex;
std::atomic<bool> shutdown_requested{false};

void on_switch_state_change(_In_ sai_object_id_t switch_id,
    _In_ sai_switch_oper_status_t switch_oper_status) {
}

void on_fdb_event(_In_ uint32_t count,
    _In_ sai_fdb_event_notification_data_t *data) {
  if (data == nullptr) return;
  std::lock_guard<std::mutex> lock(gFdbMutex);
  // SAI may batch notifications. Each record has its own attribute list;
  // flush notifications may omit a bridge-port selector (meaning all ports).
  for (uint32_t index = 0; index < count; ++index) {
    const auto &notification = data[index];
    const auto &entry = notification.fdb_entry;
    sai_object_id_t bridge_port = SAI_NULL_OBJECT_ID;
    for (uint32_t i = 0; i < notification.attr_count; ++i) {
      if (notification.attr[i].id == SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID)
        bridge_port = notification.attr[i].value.oid;
    }
    const auto same_key = [&entry](const std::pair<sai_fdb_entry_t, sai_object_id_t> &item) {
      return item.first.switch_id == entry.switch_id &&
             item.first.bv_id == entry.bv_id &&
             std::memcmp(item.first.mac_address, entry.mac_address, 6) == 0;
    };
    switch (notification.event_type) {
    case SAI_FDB_EVENT_LEARNED:
    case SAI_FDB_EVENT_MOVE: {
      auto it = std::find_if(gFdbMap.begin(), gFdbMap.end(), same_key);
      if (it == gFdbMap.end()) gFdbMap.emplace_back(entry, bridge_port);
      else it->second = bridge_port;
      break;
    }
    case SAI_FDB_EVENT_AGED:
      gFdbMap.erase(std::remove_if(gFdbMap.begin(), gFdbMap.end(), same_key), gFdbMap.end());
      break;
    case SAI_FDB_EVENT_FLUSHED:
      gFdbMap.erase(std::remove_if(gFdbMap.begin(), gFdbMap.end(),
          [&entry, bridge_port](const std::pair<sai_fdb_entry_t, sai_object_id_t> &item) {
            return (entry.bv_id == SAI_NULL_OBJECT_ID || item.first.bv_id == entry.bv_id) &&
                   (bridge_port == SAI_NULL_OBJECT_ID || item.second == bridge_port);
          }), gFdbMap.end());
      break;
    default:
      break;
    }
  }
}

void on_port_state_change(_In_ uint32_t count,
    _In_ sai_port_oper_status_notification_t *data) {
}

void on_shutdown_request(_In_ sai_object_id_t switch_id) {
  shutdown_requested.store(true); // SDK callback: no SAI or joining here.
}
