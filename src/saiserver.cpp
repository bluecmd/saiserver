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

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include "switch_sai_rpc.h"
#include "switch_sai_rpc_server.h"

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

sai_object_id_t gSwitchId; ///< SAI switch global object ID.

void on_switch_state_change(_In_ sai_object_id_t switch_id,
    _In_ sai_switch_oper_status_t switch_oper_status) {
}

void on_fdb_event(_In_ uint32_t count,
    _In_ sai_fdb_event_notification_data_t *data) {
  sai_fdb_event_t event_type;
  sai_fdb_entry_t fdb_entry;
  uint32_t attr_count;
  sai_attribute_t *attr;
  sai_object_id_t bv_id;
  sai_object_id_t bport_id;

  attr = data->attr;
  event_type = data->event_type;
  fdb_entry = data->fdb_entry;
  bv_id = fdb_entry.bv_id;
  attr_count = data ->attr_count;

  for (uint32_t i = 0; i < attr_count; i++) {
    if (attr[i].id == SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID) {
      bport_id = attr[i].value.oid;
    }
  }

  sai_fdb_entry_t fdb_m;
  sai_object_id_t b_id;

  switch (event_type) {
  case SAI_FDB_EVENT_LEARNED:
    gFdbMap.emplace_back(std::pair<sai_fdb_entry_t, sai_object_id_t>(fdb_entry,bport_id));
    break;
  case SAI_FDB_EVENT_FLUSHED:
    if (bv_id == 0 && bport_id == 0) {
      gFdbMap.clear();
    } else {
      for (auto it = gFdbMap.begin(); it != gFdbMap.end(); ) {
        fdb_m = it->first;
        b_id = it->second;

        if (bport_id == 0 && bv_id == fdb_m.bv_id) {
          it = gFdbMap.erase(it);
        } else if (bv_id == 0 && bport_id == b_id) {
          it = gFdbMap.erase(it);
        } else if (bv_id == fdb_m.bv_id && bport_id == b_id) {
          it = gFdbMap.erase(it);
        } else {
          it++;
        }
      }
    }
    break;
  case SAI_FDB_EVENT_MOVE:
    for (auto it = gFdbMap.begin(); it != gFdbMap.end(); it++) {
      fdb_m = it->first;
      b_id = it->second;
      int n = memcmp ( fdb_entry.mac_address, fdb_m.mac_address, 6);

      if (n == 0 && bv_id == fdb_m.bv_id) {
        it->second = bport_id;
      }
    }
    break;
  case SAI_FDB_EVENT_AGED:
    for (auto it = gFdbMap.begin(); it != gFdbMap.end(); ) {
      fdb_m = it->first;
      b_id = it->second;
      int n = memcmp ( fdb_entry.mac_address, fdb_m.mac_address, 6);

      if (n == 0 && bv_id == fdb_m.bv_id) {
        it = gFdbMap.erase(it);
      } else {
        it++;
      }
    }
    break;
  default:
    printf("unknown event");
    break;
  }
}

void on_port_state_change(_In_ uint32_t count,
    _In_ sai_port_oper_status_notification_t *data) {
}

void on_shutdown_request(_In_ sai_object_id_t switch_id) {
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
  while (true) {
    sai_attribute_t attr;
    attr.id = SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE;
    attr.value.booldata = true;
    status = sai_switch_api->set_switch_attribute(gSwitchId, &attr);
    if (status != SAI_STATUS_SUCCESS) {
      printf("Could not start vendor specific diagnostic shell\n");
      return;
    }

    sleep(1);
  }
}

struct cmdOptions {
  std::string profileMapFile;
};

cmdOptions handleCmdLine(int argc, char **argv) {

  cmdOptions options = {};

  while(true) {
    static struct option long_options[] = {
      { "profile",          required_argument, 0, 'p' },
      { 0,                  0,                 0,  0  }
    };

    int option_index = 0;

    int c = getopt_long(argc, argv, "p:f:S:", long_options, &option_index);

    if (c == -1) {
      break;
    }

    switch (c) {
    case 'p':
      printf("profile map file: %s\n", optarg);
      options.profileMapFile = std::string(optarg);
      break;

    default:
      fprintf(stderr, "Usage: %s [-p sai.profile]\n", argv[0]);
      exit(EXIT_FAILURE);
    }
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

    if (failed > 0) {
      printf("SAI_API_SWITCH failed for %d apis", failed);
      exit(EXIT_FAILURE);
    }
  } else {
    printf("FATAL: failed to sai_api_initialize: %d", status);
    exit(EXIT_FAILURE);
  }

  constexpr std::uint32_t attrSz = 6;

  sai_attribute_t attr[attrSz];

  std::memset(attr, '\0', sizeof(attr));

  attr[0].id = SAI_SWITCH_ATTR_INIT_SWITCH;
  attr[0].value.booldata = true;

  sai_mac_t mac = {0x11, 0x22, 0x33, 0x44, 0x55, 0x66};

  // NOTE: Seems like Broadcom SAI at least requires the MAC to be set
  // when init'ing or it will return SAI_STATUS_FAILURE.
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

  status = sai_switch_api->create_switch(&gSwitchId, attrSz, attr);
  if (status != SAI_STATUS_SUCCESS) {
    printf("Error: Failed to create switch: %d \n", status);
    exit(EXIT_FAILURE);
  }

  std::thread diag_shell_thread = std::thread(sai_diag_shell);
  diag_shell_thread.detach();

  start_sai_thrift_rpc_server(SWITCH_SAI_THRIFT_RPC_SERVER_PORT);

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

  while (true) {
    pause();
  }

  return 0;
}
