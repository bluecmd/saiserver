#include <errno.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/queue.h>
#include <sys/types.h>
#include <algorithm>
#include <fstream>
#include <sstream>
#include <set>
#include <iostream>
#include <getopt.h>
#include <assert.h>
#include <signal.h>

#include <cstring>
#include <thread>
#include <mutex>

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include "switch_sai_rpc.h"
#include "switch_sai_rpc_server.h"
#include "tui_rpc.h"
#include <atomic>
#include <chrono>

extern "C" {
#include "sai.h"
#include "saistatus.h"
#include "saiversion.h"
}


#define SWITCH_SAI_THRIFT_RPC_SERVER_PORT 9090

typedef struct {
  const char* sai_api_version;
  const char* bcm_sai_version;
  const char* build_release;
  /* these are only populated after create_switch */
  const char* cancun_version;
  const char* npl_version;
} brcm_sai_version_t;

extern "C" {
extern brcm_sai_version_t* brcm_sai_version_get(brcm_sai_version_t*) __attribute__((weak));
extern void ifcs_get_version(int* major, int* minor, int* rev) __attribute__((weak));
}

sai_switch_api_t* sai_switch_api;

std::map<std::string, std::string> gProfileMap;

extern std::vector<std::pair<sai_fdb_entry_t, sai_object_id_t>> gFdbMap;
std::mutex gFdbMutex;

sai_object_id_t gSwitchId; ///< SAI switch global object ID.
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

// Profile services
/* Get variable value given its name */
const char* test_profile_get_value(
    _In_ sai_switch_profile_id_t profile_id,
    _In_ const char* variable) {

  if (variable == NULL) {
    printf("variable is null\n");
    return NULL;
  }

  std::map<std::string, std::string>::const_iterator it = gProfileMap.find(variable);
  if (it == gProfileMap.end()) {
    printf("%s: NULL\n", variable);
    return NULL;
  }

  return it->second.c_str();
}

std::map<std::string, std::string>::iterator gProfileIter = gProfileMap.begin();
/* Enumerate all the K/V pairs in a profile.
   Pointer to NULL passed as variable restarts enumeration.
   Function returns 0 if next value exists, -1 at the end of the list. */
int test_profile_get_next_value(
    _In_ sai_switch_profile_id_t profile_id,
    _Out_ const char** variable,
    _Out_ const char** value) {

  if (value == NULL) {
    printf("resetting profile map iterator");

    gProfileIter = gProfileMap.begin();
    return 0;
  }

  if (variable == NULL) {
    printf("variable is null");
    return -1;
  }

  if (gProfileIter == gProfileMap.end()) {
    printf("iterator reached end");
    return -1;
  }

  *variable = gProfileIter->first.c_str();
  *value = gProfileIter->second.c_str();

  printf("key: %s:%s", *variable, *value);

  gProfileIter++;

  return 0;
}

const sai_service_method_table_t test_services = {
  test_profile_get_value,
  test_profile_get_next_value
};

void sai_diag_shell() {
  sai_status_t status;

  // Allow the system to start up and the console to calm down
  sleep(2);
  while (!shutdown_requested.load()) {
    status = tui_rpc::diagnostic_shell(gSwitchId);
    if (status != SAI_STATUS_SUCCESS) {
      printf("Could not start vendor specific diagnostic shell\n");
      return;
    }

    sleep(1);
  }
}

struct cmdOptions {
  std::string profileMapFile;
  bool diagnosticShell = true;
  interface_address::Options addresses;
};

cmdOptions handleCmdLine(int argc, char **argv) {

  cmdOptions options = {};

  while(true) {
    static struct option long_options[] = {
      { "profile",          required_argument, 0, 'p' },
      { "no-shell",         no_argument,       0, 'n' },
      { "interface-address", no_argument, 0, 1000 },
      { "interface-address-static-ipv6-no-dad", no_argument, 0, 1001 },
      { "interface-address-allow-unpoliced-cpu", no_argument, 0, 1002 },
      { "interface-address-policer", required_argument, 0, 1003 },
      { 0,                  0,                 0,  0  }
    };

    int option_index = 0;

    int c = getopt_long(argc, argv, "p:n", long_options, &option_index);

    if (c == -1) {
      break;
    }

    switch (c) {
    case 'p':
      printf("profile map file: %s\n", optarg);
      options.profileMapFile = std::string(optarg);
      break;

    case 'n':
      options.diagnosticShell = false;
      break;

    case 1000: options.addresses.enabled = true; break;
    case 1001: options.addresses.static_ipv6_no_dad = true; break;
    case 1002: options.addresses.allow_unpoliced_cpu = true; break;
    case 1003: {
      // Only decimal or 0x hexadecimal, no signs, whitespace or trailing bytes.
      const std::string text(optarg);
      size_t pos = text.compare(0, 2, "0x") == 0 ? 2 : 0;
      const unsigned base = pos ? 16 : 10;
      uint64_t value = 0;
      bool valid = pos < text.size();
      for (; pos < text.size(); ++pos) {
        char c = text[pos];
        unsigned d = c >= '0' && c <= '9' ? c - '0' :
          c >= 'a' && c <= 'f' ? c - 'a' + 10 : c >= 'A' && c <= 'F' ? c - 'A' + 10 : 99;
        if (d >= base || value > (UINT64_MAX - d) / base) { valid = false; break; }
        value = value * base + d;
      }
      if (!valid || !value) { fprintf(stderr, "Invalid nonzero policer OID\n"); exit(EXIT_FAILURE); }
      options.addresses.policer = value; break;
    }
    default:
      fprintf(stderr, "Usage: %s [-p sai.profile] [--no-shell] [--interface-address "
          "--interface-address-static-ipv6-no-dad "
          "(--interface-address-allow-unpoliced-cpu | --interface-address-policer OID)]\n", argv[0]);
      exit(EXIT_FAILURE);
    }
  }

  if (optind != argc ||
      (options.addresses.enabled && (!options.addresses.static_ipv6_no_dad ||
        (!options.addresses.allow_unpoliced_cpu && !options.addresses.policer))) ||
      (!options.addresses.enabled && (options.addresses.static_ipv6_no_dad ||
        options.addresses.allow_unpoliced_cpu || options.addresses.policer))) {
    fprintf(stderr, "interface_address requires explicit enable, STATIC IPv6 NO DAD acknowledgement "
        "(operator guarantees unique addresses), and a valid supplied policer or "
        "software-only admission acknowledgement (NO ASIC CPU policer).\n");
    exit(EXIT_FAILURE);
  }
  if (options.addresses.enabled) {
    options.diagnosticShell = false;
    fprintf(stderr, "interface_address: bounded-only RPCs; diagnostic shell disabled; "
        "STATIC IPv6 NO DAD. Software responder, NOT hardware-verified. "
        "Full Ethernet/tag preservation by SDK callbacks is unverified.\n");
    if (!options.addresses.policer)
      fprintf(stderr, "WARNING: software-only admission; NO ASIC CPU policer/rate guarantee.\n");
  }
  return options;
}

void handleProfileMap(const std::string& profileMapFile) {

  if (profileMapFile.size() == 0) {
    return;
  }

  std::ifstream profile(profileMapFile);

  if (!profile.is_open()) {
    printf("failed to open profile map file: %s : %s\n", profileMapFile.c_str(), strerror(errno));
    exit(EXIT_FAILURE);
  }

  std::string line;

  while(getline(profile, line)) {
    if (line.size() > 0 && (line[0] == '#' || line[0] == ';')) {
      continue;
    }

    size_t pos = line.find("=");

    if (pos == std::string::npos) {
      printf("not found '=' in line %s\n", line.c_str());
      continue;
    }

    std::string key = line.substr(0, pos);
    std::string value = line.substr(pos + 1);

    gProfileMap[key] = value;

    printf("insert: %s:%s\n", key.c_str(), value.c_str());
  }
}

int main(int argc, char* argv[]) {
  sai_api_version_t version;
  auto options = handleCmdLine(argc, argv);
  // Block before spawning any SDK/worker threads; main consumes signals with
  // sigtimedwait. No async signal handler ever calls SAI or joins a thread.
  sigset_t signals; sigemptyset(&signals); sigaddset(&signals, SIGINT); sigaddset(&signals, SIGTERM);
  if (pthread_sigmask(SIG_BLOCK, &signals, nullptr) != 0) return EXIT_FAILURE;
  handleProfileMap(options.profileMapFile);

  if (sai_query_api_version(&version) == SAI_STATUS_SUCCESS) {
    int major = version / 10000;
    int minor = (version - major * 10000) / 100;
    int rev = version - major * 10000 - minor * 100;
    printf("================================\n");
    printf("  Loaded SAI version %d.%d.%d\n", major, minor, rev);
  }

  if (brcm_sai_version_get != NULL) {
    brcm_sai_version_t brcm_version;
    brcm_sai_version_get(&brcm_version);
    printf(
        "\n  Broadcom SAI detected\n    SAI API version: %s\n    BRCM SAI version: %s\n    Build release: %s\n",
        brcm_version.sai_api_version,
        brcm_version.bcm_sai_version,
        brcm_version.build_release);
  }

  if (ifcs_get_version != NULL) {
    int major = 0;
    int minor = 0;
    int rev = 0;
    ifcs_get_version(&major, &minor, &rev);
    printf(
        "\n  Innovium SAI detected\n    IFCS version: %d.%d.%d\n",
        major, minor, rev);
  }

  printf("================================\n");

  auto status = sai_api_initialize(0, (sai_service_method_table_t *)&test_services);
  if (status == SAI_STATUS_SUCCESS) {
    int failed = sai_api_query(SAI_API_SWITCH, (void**)&sai_switch_api);

    if (failed != SAI_STATUS_SUCCESS) {
      printf("SAI_API_SWITCH failed for %d apis", failed);
      exit(EXIT_FAILURE);
    }
  } else {
    printf("FATAL: failed to sai_api_initialize: %d", status);
    exit(EXIT_FAILURE);
  }

  const std::uint32_t attrSz = options.addresses.enabled ? 7 : 6;

  sai_attribute_t attr[7];

  std::memset(attr, '\0', sizeof(attr));

  attr[0].id = SAI_SWITCH_ATTR_INIT_SWITCH;
  attr[0].value.booldata = true;

  // Broadcom SAI requires a source MAC when initializing. Use the tested
  // locally administered unicast default (the historical 0x11 is multicast),
  // while allowing deployments to choose their own address via SAI_SRC_MAC.
  sai_mac_t mac = {0x02, 0x00, 0x00, 0x00, 0x04, 0x01};
  const char* src_mac_env = getenv("SAI_SRC_MAC");
  if (src_mac_env != nullptr && src_mac_env[0] != '\0') {
    unsigned int b[6];
    char tail = 0;
    if (sscanf(src_mac_env, "%2x:%2x:%2x:%2x:%2x:%2x%c",
               &b[0], &b[1], &b[2], &b[3], &b[4], &b[5], &tail) != 6) {
      fprintf(stderr, "SAI_SRC_MAC must be six colon-separated hex bytes, got %s\n",
              src_mac_env);
      exit(EXIT_FAILURE);
    }
    for (int i = 0; i < 6; i++) {
      mac[i] = static_cast<unsigned char>(b[i]);
    }
  }
  printf("Switch source MAC: %02x:%02x:%02x:%02x:%02x:%02x\n",
         mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);

  attr[1].id = SAI_SWITCH_ATTR_SRC_MAC_ADDRESS;
  memcpy(attr[1].value.mac, mac, sizeof(mac));

  attr[2].id = SAI_SWITCH_ATTR_SWITCH_STATE_CHANGE_NOTIFY;
  attr[2].value.ptr = reinterpret_cast<sai_pointer_t>(&on_switch_state_change);

  attr[3].id = SAI_SWITCH_ATTR_SHUTDOWN_REQUEST_NOTIFY;
  attr[3].value.ptr = reinterpret_cast<sai_pointer_t>(&on_shutdown_request);

  attr[4].id = SAI_SWITCH_ATTR_FDB_EVENT_NOTIFY;
  attr[4].value.ptr = reinterpret_cast<sai_pointer_t>(&on_fdb_event);

  attr[5].id = SAI_SWITCH_ATTR_PORT_STATE_CHANGE_NOTIFY;
  attr[5].value.ptr = reinterpret_cast<sai_pointer_t>(&on_port_state_change);

  if (options.addresses.enabled) {
    attr[6].id = SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY;
    attr[6].value.ptr = reinterpret_cast<sai_pointer_t>(interface_address::packet_callback());
  }
  try { status = tui_rpc::create_switch(&gSwitchId, attrSz, attr); }
  catch (const sai_tui::RpcError& e) { status = e.status; }
  if (status != SAI_STATUS_SUCCESS) {
    fprintf(stderr, "Error: Failed to create switch: %d\n", status);
    // No worker or RPC thread exists yet; never retry switch creation.
    const auto teardown = sai_api_uninitialize();
    if (teardown != SAI_STATUS_SUCCESS) {
      fprintf(stderr, "SDK teardown after create failure FAILED: %d\n", teardown);
      fflush(nullptr); std::_Exit(EXIT_FAILURE);
    }
    return EXIT_FAILURE;
  }

  int result = EXIT_SUCCESS;
  bool responder_start_attempted = false, responder_started = false;
  std::thread diag_shell_thread;
  try {
    if (options.addresses.enabled) {
      interface_address::Sdk sdk;
      sdk.query = &sai_api_query; sdk.keys = &sai_get_object_key;
      sdk.object_type = &sai_object_type_query; sdk.switch_id = &sai_switch_id_query;
      sdk.enum_values = &sai_query_attribute_enum_values_capability;
      // start reads back the preinstalled callback and verifies SDK support.
      // No RPC endpoint is available until this succeeds.
      responder_start_attempted = true;
      tui_rpc::start_interface_addresses(gSwitchId, options.addresses, sdk);
      responder_started = true;
    }
    if (options.diagnosticShell) diag_shell_thread = std::thread(sai_diag_shell);
    if (start_sai_thrift_rpc_server(SWITCH_SAI_THRIFT_RPC_SERVER_PORT) != 0)
      throw std::runtime_error("RPC server startup failed");

    const sai_log_level_t log_level = SAI_LOG_LEVEL_NOTICE;

    sai_log_set(SAI_API_ACL, log_level);
    sai_log_set(SAI_API_BRIDGE, log_level);
    sai_log_set(SAI_API_BUFFER, log_level);
    sai_log_set(SAI_API_DEBUG_COUNTER, log_level);
    sai_log_set(SAI_API_FDB, log_level);
    sai_log_set(SAI_API_HOSTIF, log_level);
    sai_log_set(SAI_API_LAG, log_level);
    sai_log_set(SAI_API_MIRROR, log_level);
    sai_log_set(SAI_API_NEIGHBOR, log_level);
    sai_log_set(SAI_API_NEXT_HOP, log_level);
    sai_log_set(SAI_API_NEXT_HOP_GROUP, log_level);
    sai_log_set(SAI_API_POLICER, log_level);
    sai_log_set(SAI_API_PORT, log_level);
    sai_log_set(SAI_API_QOS_MAP, log_level);
    sai_log_set(SAI_API_ROUTE, log_level);
    sai_log_set(SAI_API_ROUTER_INTERFACE, log_level);
    sai_log_set(SAI_API_SWITCH, log_level);
    sai_log_set(SAI_API_TUNNEL, log_level);
    sai_log_set(SAI_API_VIRTUAL_ROUTER, log_level);
    sai_log_set(SAI_API_VLAN, log_level);
    sai_log_set(SAI_API_WRED, log_level);

    while (!shutdown_requested.load() && sai_thrift_rpc_server_running()) {
      timespec timeout{0, 100000000};
      int signal = sigtimedwait(&signals, nullptr, &timeout);
      if (signal == SIGINT || signal == SIGTERM) shutdown_requested.store(true);
    }
    if (!shutdown_requested.load()) result = EXIT_FAILURE;
  } catch (const interface_address::Error& e) {
    fprintf(stderr, "interface_address startup failed status %d: %s\n", e.status, e.what());
    result = EXIT_FAILURE;
  } catch (const sai_tui::RpcError& e) {
    fprintf(stderr, "Server failed status %d: %s\n", e.status, e.message.c_str()); result = EXIT_FAILURE;
  } catch (const std::exception& e) {
    fprintf(stderr, "Server failed: %s\n", e.what()); result = EXIT_FAILURE;
  }
  shutdown_requested.store(true);
  stop_sai_thrift_rpc_server();
  if (diag_shell_thread.joinable()) diag_shell_thread.join();
  // start() failure already stopped admission and rolled back without starting
  // a worker. Do not automatically retry failed rollback removals on this path.
  if (responder_start_attempted && !responder_started) {
    const auto s = interface_address::status();
    if (s.trap_group || s.traps[0] || s.traps[1] || s.tables[0] || s.tables[1])
      fprintf(stderr, "Startup rollback incomplete status %d: %s; residual group=%llx "
          "traps=%llx,%llx tables=%llx,%llx; no automatic retry\n", s.last_status, s.last_error.c_str(),
          (unsigned long long)s.trap_group, (unsigned long long)s.traps[0], (unsigned long long)s.traps[1],
          (unsigned long long)s.tables[0], (unsigned long long)s.tables[1]);
  } else try { tui_rpc::stop_interface_addresses(); }
  catch (const interface_address::Error& e) {
    const auto s = interface_address::status();
    fprintf(stderr, "interface_address cleanup FAILED status %d: %s; residual group=%llx "
        "traps=%llx,%llx tables=%llx,%llx; no automatic retry\n", e.status, e.what(),
        (unsigned long long)s.trap_group, (unsigned long long)s.traps[0], (unsigned long long)s.traps[1],
        (unsigned long long)s.tables[0], (unsigned long long)s.tables[1]);
    result = EXIT_FAILURE; // Preserve even if SDK teardown subsequently succeeds.
  }
  bool sdk_quiesced = false;
  try {
    status = tui_rpc::shutdown_switch(gSwitchId);
    sdk_quiesced = status == SAI_STATUS_SUCCESS;
    if (status != SAI_STATUS_SUCCESS) {
      fprintf(stderr, "SDK teardown FAILED status %d; callbacks remain resident until process exit\n", status);
      result = EXIT_FAILURE;
    }
  } catch (const sai_tui::RpcError& e) {
    fprintf(stderr, "SDK teardown FAILED status %d: %s\n", e.status, e.message.c_str());
    result = EXIT_FAILURE;
  }
  // If the SDK failed to quiesce, do not run C++ static destructors while
  // vendor threads may still invoke our callback (even a no-op uses its state).
  // Keep code AND callback state resident until the OS terminates the process.
  if (!sdk_quiesced) { fflush(nullptr); std::_Exit(EXIT_FAILURE); }
  return result;
}
