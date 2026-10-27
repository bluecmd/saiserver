// Bounded, getter-backed management service. No legacy parsers are used.
#pragma once
#include "sai_tui_types.h"
#include <map>
#include <string>
#include <cstdint>

namespace tui_rpc {
void snapshot(sai_tui::Inventory&, uint64_t switch_id);
void get(sai_tui::Object&, uint64_t switch_id, const std::string& kind, const std::string& key);
void create(sai_tui::Object&, uint64_t switch_id, const std::string& kind,
            const std::map<std::string, std::string>& attributes);
void set(sai_tui::Object&, uint64_t switch_id, const std::string& kind, const std::string& key,
         const std::map<std::string, std::string>& attributes);
void remove(uint64_t switch_id, const std::string& kind, const std::string& key);
void port_counters(std::map<std::string, int64_t>&, uint64_t switch_id, const std::string& key);
}
