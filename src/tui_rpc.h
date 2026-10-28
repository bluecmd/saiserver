// Bounded, getter-backed management service. No legacy parsers are used.
#pragma once
#include "sai_tui_types.h"
#include "src/interface_address.h"
#include <map>
#include <string>
#include <cstdint>

namespace tui_rpc {
// Lifecycle calls are made before accepting RPCs / after joining the RPC server.
// All SAI calls below share the responder's topology mutex.
sai_status_t create_switch(sai_object_id_t*, uint32_t, const sai_attribute_t*);
void start_interface_addresses(sai_object_id_t, const interface_address::Options&,
                               const interface_address::Sdk&);
void stop_interface_addresses();
sai_status_t shutdown_switch(sai_object_id_t); // unregister ours, remove, uninitialize
sai_status_t diagnostic_shell(sai_object_id_t);
bool bounded_only() noexcept; // sticky once opt-in attempted; includes faulted state
void snapshot(sai_tui::Inventory&, uint64_t switch_id);
void get(sai_tui::Object&, uint64_t switch_id, const std::string& kind, const std::string& key);
void create(sai_tui::Object&, uint64_t switch_id, const std::string& kind,
            const std::map<std::string, std::string>& attributes);
void set(sai_tui::Object&, uint64_t switch_id, const std::string& kind, const std::string& key,
         const std::map<std::string, std::string>& attributes);
void remove(uint64_t switch_id, const std::string& kind, const std::string& key);
void port_counters(std::map<std::string, int64_t>&, uint64_t switch_id, const std::string& key);
}
