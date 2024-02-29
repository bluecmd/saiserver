/*
   Copyright 2013 Barefoot Networks, Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

#include <cstddef>
#include <cstdint>
#include <cstring>
#include <ctime>

#include <iostream>
#include <sstream>
#include <fstream>

#include <string>
#include <vector>

#include <iomanip>

#include <iostream>
#include <string>
#include "switch_sai_rpc.h"
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/server/TSimpleServer.h>
#include <thrift/transport/TServerSocket.h>
#include <thrift/transport/TBufferTransports.h>
#include <arpa/inet.h>

#include <inttypes.h>

#ifdef __cplusplus
extern "C" {
#endif
#include <sai.h>
#ifdef __cplusplus
}
#endif

#include <saifdb.h>
#include <saivlan.h>
#include <sairouterinterface.h>
#include <sairoute.h>
#include <saiswitch.h>
#include <saimirror.h>
#include <saistatus.h>
#include <saitunnel.h>
#include <saisystemport.h>

#include "arpa/inet.h"

#define SAI_THRIFT_LOG_DBG(...) sai_thrift_timestamp_print(); \
  printf("SAI THRIFT DEBUG: %s(): ", __FUNCTION__); printf(__VA_ARGS__); printf("\n");

#define SAI_THRIFT_LOG_ERR(...) sai_thrift_timestamp_print(); \
  printf("SAI THRIFT ERROR: %s(): ", __FUNCTION__); printf(__VA_ARGS__); printf("\n");

#define SAI_THRIFT_FUNC_LOG() SAI_THRIFT_LOG_DBG("Called.")

using namespace ::apache::thrift;
using namespace ::apache::thrift::protocol;
using namespace ::apache::thrift::transport;
using namespace ::apache::thrift::server;

using std::shared_ptr;

using namespace ::switch_sai;

extern sai_object_id_t gSwitchId;

typedef std::vector<sai_thrift_attribute_t> std_sai_thrift_attr_vctr_t;

std::vector<std::pair<sai_fdb_entry_t, sai_object_id_t>>gFdbMap;

class switch_sai_rpcHandler : virtual public switch_sai_rpcIf {
  public:
    switch_sai_rpcHandler() noexcept {
    }

    inline void sai_thrift_timestamp_print() const noexcept {
      const auto ltime = std::time(nullptr);
      const auto tm = std::localtime(&ltime);

      std::printf("%02d:%02d:%02d ", tm->tm_hour, tm->tm_min, tm->tm_sec);
    }

    template<typename T>
      inline void sai_thrift_alloc_array(T* &arr, const std::size_t &size) const noexcept {
        arr = new (std::nothrow) T[size];
      }

    template<typename T>
      inline void sai_thrift_free_array(T* &arr) const noexcept {
        delete[] arr;
        arr = nullptr;
      }

    unsigned int sai_thrift_string_to_mac(const std::string s, unsigned char *m) {
      unsigned int i, j=0;
      memset(m, 0, 6);
      for (i=0;i<s.size();i++) {
        char let = s.c_str()[i];
        if (let >= '0' && let <= '9') {
          m[j/2] = (m[j/2] << 4) + (let - '0'); j++;
        } else if (let >= 'a' && let <= 'f') {
          m[j/2] = (m[j/2] << 4) + (let - 'a'+10); j++;
        } else if (let >= 'A' && let <= 'F') {
          m[j/2] = (m[j/2] << 4) + (let - 'A'+10); j++;
        }
      }
      return (j == 12);
    }

    const std::string mac_to_sai_thrift_string(uint8_t m[6]) {
      char macstr[32];
      sprintf(macstr, "%02x:%02x:%02x:%02x:%02x:%02x", m[0], m[1], m[2], m[3], m[4], m[5]);
      return(macstr);
    }

    void sai_thrift_string_to_v4_ip(const std::string s, unsigned int *m) {
      unsigned char r=0;
      unsigned int i;
      *m = 0;
      for (i=0;i<s.size();i++) {
        char let = s.c_str()[i];
        if (let >= '0' && let <= '9') {
          r = (r * 10) + (let - '0');
        } else {
          *m = (*m << 8) | r;
          r=0;
        }
      }
      *m = (*m << 8) | (r & 0xFF);
      *m = htonl(*m);
      return;
    }

    void sai_thrift_string_to_v6_ip(const std::string s, unsigned char *v6_ip) {
      const char *v6_str = s.c_str();
      inet_pton(AF_INET6, v6_str, v6_ip);
      return;
    }

    inline void sai_thrift_alloc_attr(sai_attribute_t* &attr, const sai_uint32_t &size) const noexcept {
      attr = new (std::nothrow) sai_attribute_t[size];
    }

    inline void sai_thrift_free_attr(sai_attribute_t* &attr) const noexcept {
      delete[] attr;
      attr = nullptr;
    }

    void sai_thrift_parse_object_id_list(const std::vector<sai_thrift_object_id_t> & thrift_object_id_list, sai_object_id_t *object_id_list) {
      std::vector<sai_thrift_object_id_t>::const_iterator it = thrift_object_id_list.begin();
      for (uint32_t i = 0; i < thrift_object_id_list.size(); i++, it++) {
        object_id_list[i] = (sai_object_id_t)*it;
      }
    }

    void sai_thrift_parse_ip_address(const sai_thrift_ip_address_t &thrift_ip_address, sai_ip_address_t *ip_address) {
      ip_address->addr_family = (sai_ip_addr_family_t) thrift_ip_address.addr_family;
      if ((sai_ip_addr_family_t)thrift_ip_address.addr_family == SAI_IP_ADDR_FAMILY_IPV4) {
        sai_thrift_string_to_v4_ip(thrift_ip_address.addr.ip4, &ip_address->addr.ip4);
      } else {
        sai_thrift_string_to_v6_ip(thrift_ip_address.addr.ip6, ip_address->addr.ip6);
      }
    }

    void sai_thrift_parse_ip_prefix(const sai_thrift_ip_prefix_t &thrift_ip_prefix, sai_ip_prefix_t *ip_prefix) {
      ip_prefix->addr_family = (sai_ip_addr_family_t) thrift_ip_prefix.addr_family;
      if ((sai_ip_addr_family_t)thrift_ip_prefix.addr_family == SAI_IP_ADDR_FAMILY_IPV4) {
        sai_thrift_string_to_v4_ip(thrift_ip_prefix.addr.ip4, &ip_prefix->addr.ip4);
        sai_thrift_string_to_v4_ip(thrift_ip_prefix.mask.ip4, &ip_prefix->mask.ip4);
      } else {
        sai_thrift_string_to_v6_ip(thrift_ip_prefix.addr.ip6, ip_prefix->addr.ip6);
        sai_thrift_string_to_v6_ip(thrift_ip_prefix.mask.ip6, ip_prefix->mask.ip6);
      }
    }

    void sai_thrift_parse_attribute_ids(const std::vector<int32_t> &thrift_attr_id_list, sai_attribute_t *attr_list) {
      std::vector<int32_t>::const_iterator it = thrift_attr_id_list.begin();
      for (uint32_t i = 0; i < thrift_attr_id_list.size(); i++, it++) {
        attr_list[i].id = (int32_t) *it;
      }
    }

    sai_attribute_t *sai_thrift_attribute_list_to_sai(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_attribute_t *sai_attrs;

      sai_attrs = (sai_attribute_t *) calloc(thrift_attr_list.size(), sizeof(sai_attribute_t));
      if (!sai_attrs) {
        SAI_THRIFT_LOG_ERR("failed to allocate sai attributes list");
        return NULL;
      }

      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        sai_thrift_attribute_t & thrift_attr = (sai_thrift_attribute_t &) *it;
        sai_attrs[i].id = thrift_attr.id;
        sai_attrs[i].value.oid = thrift_attr.value.oid;
      }

      return sai_attrs;
    }

    void sai_attributes_to_sai_thrift_list(sai_attribute_t *sai_attrs, uint32_t count, std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      for (uint32_t i = 0; i < count; i++) {
        sai_thrift_attribute_t thrift_attr;

        thrift_attr.id        = sai_attrs[i].id;
        thrift_attr.value.oid = sai_attrs[i].value.oid;

        thrift_attr_list.push_back(thrift_attr);
      }
    }

    void sai_thrift_parse_fdb_entry(const sai_thrift_fdb_entry_t &thrift_fdb_entry, sai_fdb_entry_t *fdb_entry) {
      fdb_entry->bv_id = (sai_object_id_t) thrift_fdb_entry.bv_id;
      sai_thrift_string_to_mac(thrift_fdb_entry.mac_address, fdb_entry->mac_address);
    }

    void sai_thrift_parse_route_entry(const sai_thrift_route_entry_t &thrift_route_entry, sai_route_entry_t *route_entry) {
      route_entry->switch_id = gSwitchId;
      route_entry->vr_id = (sai_object_id_t) thrift_route_entry.vr_id;
      sai_thrift_parse_ip_prefix(thrift_route_entry.destination, &route_entry->destination);
    }

    void sai_thrift_parse_neighbor_entry(const sai_thrift_neighbor_entry_t &thrift_neighbor_entry, sai_neighbor_entry_t *neighbor_entry) {
      neighbor_entry->switch_id = gSwitchId;
      neighbor_entry->rif_id = (sai_object_id_t) thrift_neighbor_entry.rif_id;
      sai_thrift_parse_ip_address(thrift_neighbor_entry.ip_address, &neighbor_entry->ip_address);
    }

    void sai_thrift_parse_port_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list, sai_object_id_t **buffer_profile_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;

      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_PORT_ATTR_ADMIN_STATE:
        case SAI_PORT_ATTR_UPDATE_DSCP:
        case SAI_PORT_ATTR_PKT_TX_ENABLE:
          attr_list[i].value.booldata = attribute.value.booldata;
          break;
        case SAI_PORT_ATTR_PORT_VLAN_ID:
          attr_list[i].value.u16 = attribute.value.u16;
          break;
        case SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL:
        case SAI_PORT_ATTR_QOS_DEFAULT_TC:
          attr_list[i].value.u8 = attribute.value.u8;
          break;
        case SAI_PORT_ATTR_QOS_INGRESS_BUFFER_PROFILE_LIST:
        case SAI_PORT_ATTR_QOS_EGRESS_BUFFER_PROFILE_LIST:
          {
            *buffer_profile_list = (sai_object_id_t *) malloc(sizeof(sai_object_id_t) * attribute.value.objlist.count);
            std::vector<sai_thrift_object_id_t>::const_iterator it2 = attribute.value.objlist.object_id_list.begin();
            for (uint32_t j = 0; j < attribute.value.objlist.object_id_list.size(); j++, *it2++) {
              *buffer_profile_list[j] = (sai_object_id_t) *it2;
            }
            attr_list[i].value.objlist.count = attribute.value.objlist.count;
            attr_list[i].value.objlist.list = *buffer_profile_list;
            break;
          }
        case SAI_PORT_ATTR_INGRESS_MIRROR_SESSION:
        case SAI_PORT_ATTR_EGRESS_MIRROR_SESSION:
          {
            *buffer_profile_list = (sai_object_id_t *) malloc(sizeof(sai_object_id_t) * attribute.value.objlist.count);
            std::vector<sai_thrift_object_id_t>::const_iterator it2 = attribute.value.objlist.object_id_list.begin();
            for (uint32_t j = 0; j < attribute.value.objlist.object_id_list.size(); j++, *it2++) {
              *buffer_profile_list[j] = (sai_object_id_t) *it2;
            }
            attr_list[i].value.objlist.count = attribute.value.objlist.count;
            attr_list[i].value.objlist.list=*buffer_profile_list;
            break;
          }
        case SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID:
        case SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
        case SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
        case SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
        case SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
        case SAI_PORT_ATTR_QOS_TC_TO_QUEUE_MAP:
        case SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
        case SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
        case SAI_PORT_ATTR_QOS_TC_TO_PRIORITY_GROUP_MAP:
        case SAI_PORT_ATTR_QOS_PFC_PRIORITY_TO_PRIORITY_GROUP_MAP:
        case SAI_PORT_ATTR_QOS_PFC_PRIORITY_TO_QUEUE_MAP:
        case SAI_PORT_ATTR_INGRESS_ACL:
        case SAI_PORT_ATTR_EGRESS_ACL:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        case SAI_PORT_ATTR_MTU:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        default:
          break;
        }
      }
    }

    void sai_thrift_parse_fdb_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_FDB_ENTRY_ATTR_TYPE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        case SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        case SAI_FDB_ENTRY_ATTR_PACKET_ACTION:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        default:
          break;
        }
      }
    }

    void sai_thrift_parse_fdb_flush_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_FDB_FLUSH_ATTR_BRIDGE_PORT_ID:
          attr_list[i].value.oid = (sai_object_id_t) attribute.value.oid;
          break;
        case SAI_FDB_FLUSH_ATTR_BV_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        case SAI_FDB_FLUSH_ATTR_ENTRY_TYPE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        }
      }
    }

    void sai_thrift_parse_vr_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V4_STATE:
        case SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V6_STATE:
          attr_list[i].value.booldata = attribute.value.booldata;
          break;
        case SAI_VIRTUAL_ROUTER_ATTR_SRC_MAC_ADDRESS:
          sai_thrift_string_to_mac(attribute.value.mac, attr_list[i].value.mac);
          break;
        }
      }
    }

    void sai_thrift_parse_route_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        case SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        default:
          break;
        }
      }
    }

    void sai_thrift_parse_router_interface_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_ROUTER_INTERFACE_ATTR_VIRTUAL_ROUTER_ID:
        case SAI_ROUTER_INTERFACE_ATTR_PORT_ID:
        case SAI_ROUTER_INTERFACE_ATTR_VLAN_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        case SAI_ROUTER_INTERFACE_ATTR_OUTER_VLAN_ID:
          attr_list[i].value.u16 = attribute.value.u16;
          break;
        case SAI_ROUTER_INTERFACE_ATTR_TYPE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        case SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS:
          sai_thrift_string_to_mac(attribute.value.mac, attr_list[i].value.mac);
          break;
        case SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE:
        case SAI_ROUTER_INTERFACE_ATTR_ADMIN_V6_STATE:
          attr_list[i].value.booldata = attribute.value.booldata;
          break;
        case SAI_ROUTER_INTERFACE_ATTR_INGRESS_ACL:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        case SAI_ROUTER_INTERFACE_ATTR_MTU:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        case SAI_ROUTER_INTERFACE_ATTR_LOOPBACK_PACKET_ACTION:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        default:
          break;
        }
      }
    }

    void sai_thrift_parse_next_hop_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_NEXT_HOP_ATTR_TYPE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        case SAI_NEXT_HOP_ATTR_IP:
          sai_thrift_parse_ip_address(attribute.value.ipaddr, &attr_list[i].value.ipaddr);
          break;
        case SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID:
        case SAI_NEXT_HOP_ATTR_TUNNEL_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        }
      }
    }

    void sai_thrift_parse_lag_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it1 = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it1++) {
        attribute = (sai_thrift_attribute_t)*it1;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_LAG_ATTR_PORT_VLAN_ID:
          attr_list[i].value.u16 = attribute.value.u16;
          break;
        case SAI_LAG_ATTR_INGRESS_ACL:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        default:
          SAI_THRIFT_LOG_ERR("Failed to parse attribute.");
          break;
        }
      }
    }

    void sai_thrift_parse_lag_member_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it1 = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it1++) {
        attribute = (sai_thrift_attribute_t)*it1;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_LAG_MEMBER_ATTR_LAG_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        case SAI_LAG_MEMBER_ATTR_PORT_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        case SAI_LAG_MEMBER_ATTR_EGRESS_DISABLE:
          break;
        case SAI_LAG_MEMBER_ATTR_INGRESS_DISABLE:
          break;
        }
      }
    }

    void sai_thrift_parse_stp_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list, sai_vlan_id_t **vlan_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it1 = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it1++) {
        attribute = (sai_thrift_attribute_t)*it1;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_STP_ATTR_VLAN_LIST:
          *vlan_list = (sai_vlan_id_t *) malloc(sizeof(sai_vlan_id_t) * attribute.value.vlanlist.vlan_count);
          std::vector<sai_thrift_vlan_id_t>::const_iterator it2 = attribute.value.vlanlist.vlan_list.begin();
          for (uint32_t j = 0; j < attribute.value.vlanlist.vlan_list.size(); j++, *it2++) {
            *vlan_list[j] = (sai_vlan_id_t) *it2;
          }
          attr_list[i].value.vlanlist.count = attribute.value.vlanlist.vlan_count;
          attr_list[i].value.vlanlist.list = *vlan_list;
          break;
        }
      }
    }

    void sai_thrift_parse_neighbor_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it1 = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it1++) {
        attribute = (sai_thrift_attribute_t)*it1;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_NEIGHBOR_ENTRY_ATTR_DST_MAC_ADDRESS:
          sai_thrift_string_to_mac(attribute.value.mac, attr_list[i].value.mac);
          break;
        }
      }
    }

    void sai_thrift_parse_hostif_attributes(sai_attribute_t *attr_list, const std::vector<sai_thrift_attribute_t> &thrift_attr_list) const noexcept {
      if (attr_list == nullptr || thrift_attr_list.empty()) {
        SAI_THRIFT_LOG_ERR("Invalid input arguments.");
        return;
      }

      std::vector<sai_thrift_attribute_t>::const_iterator cit = thrift_attr_list.begin();
      for (sai_size_t i = 0; i < thrift_attr_list.size(); i++, cit++) {
        sai_thrift_attribute_t attribute = *cit;
        attr_list[i].id = attribute.id;

        switch (attribute.id) {
        case SAI_HOSTIF_ATTR_TYPE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;

        case SAI_HOSTIF_ATTR_OBJ_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;

        case SAI_HOSTIF_ATTR_NAME:
          std::memcpy(attr_list[i].value.chardata, attribute.value.chardata.c_str(), SAI_HOSTIF_NAME_SIZE);
          break;

        default:
          SAI_THRIFT_LOG_ERR("Failed to parse attribute.");
          break;
        }
      }
    }

    void sai_thrift_parse_hostif_table_entry_attributes(sai_attribute_t *attr_list, const std::vector<sai_thrift_attribute_t> &thrift_attr_list) const noexcept {
      if (attr_list == nullptr || thrift_attr_list.empty()) {
        SAI_THRIFT_LOG_ERR("Invalid input arguments.");
        return;
      }

      std::vector<sai_thrift_attribute_t>::const_iterator cit = thrift_attr_list.begin();
      for (sai_size_t i = 0; i < thrift_attr_list.size(); i++, cit++) {
        sai_thrift_attribute_t attribute = *cit;
        attr_list[i].id = attribute.id;

        switch (attribute.id) {
        case SAI_HOSTIF_TABLE_ENTRY_ATTR_TYPE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;

        case SAI_HOSTIF_TABLE_ENTRY_ATTR_OBJ_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;

        case SAI_HOSTIF_TABLE_ENTRY_ATTR_TRAP_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;

        case SAI_HOSTIF_TABLE_ENTRY_ATTR_CHANNEL_TYPE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;

        case SAI_HOSTIF_TABLE_ENTRY_ATTR_HOST_IF:
          attr_list[i].value.oid = attribute.value.oid;
          break;

        default:
          SAI_THRIFT_LOG_ERR("Failed to parse attribute.");
          break;
        }
      }
    }

    void sai_thrift_parse_hostif_trap_group_attributes(sai_attribute_t *attr_list, const std::vector<sai_thrift_attribute_t> &thrift_attr_list) const noexcept {
      if (attr_list == nullptr || thrift_attr_list.empty()) {
        SAI_THRIFT_LOG_ERR("Invalid input arguments.");
        return;
      }

      std::vector<sai_thrift_attribute_t>::const_iterator cit = thrift_attr_list.begin();

      for (sai_size_t i = 0; i < thrift_attr_list.size(); i++, cit++) {
        sai_thrift_attribute_t attribute = *cit;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_HOSTIF_TRAP_GROUP_ATTR_ADMIN_STATE:
          attr_list[i].value.booldata = attribute.value.booldata;
          break;
        case SAI_HOSTIF_TRAP_GROUP_ATTR_QUEUE:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        case SAI_HOSTIF_TRAP_GROUP_ATTR_POLICER:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        default:
          SAI_THRIFT_LOG_ERR("Failed to parse attribute.");
          break;
        }
      }
    }

    void sai_thrift_parse_hostif_trap_attributes(sai_attribute_t *attr_list, const std::vector<sai_thrift_attribute_t> &thrift_attr_list) const noexcept {
      if (attr_list == nullptr || thrift_attr_list.empty()) {
        SAI_THRIFT_LOG_ERR("Invalid input arguments.");
        return;
      }

      std::vector<sai_thrift_attribute_t>::const_iterator cit = thrift_attr_list.begin();

      for (sai_size_t i = 0; i < thrift_attr_list.size(); i++, cit++) {
        sai_thrift_attribute_t attribute = *cit;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        case SAI_HOSTIF_TRAP_ATTR_PACKET_ACTION:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        case SAI_HOSTIF_TRAP_ATTR_TRAP_PRIORITY:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        case SAI_HOSTIF_TRAP_ATTR_EXCLUDE_PORT_LIST:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        case SAI_HOSTIF_TRAP_ATTR_TRAP_GROUP:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        default:
          SAI_THRIFT_LOG_ERR("Failed to parse attribute.");
          break;
        }
      }
    }

    void sai_thrift_parse_hostif_trap_attribute(const sai_thrift_attribute_t &thrift_attr, sai_attribute_t *attr) {
      attr->id = thrift_attr.id;
      switch (thrift_attr.id) {
      case SAI_HOSTIF_TRAP_ATTR_PACKET_ACTION:
        attr->value.s32 = thrift_attr.value.s32;
        break;
      case SAI_HOSTIF_TRAP_ATTR_TRAP_PRIORITY:
        attr->value.u32 = thrift_attr.value.u32;
        break;
      case SAI_HOSTIF_TRAP_ATTR_TRAP_GROUP:
        attr->value.oid = thrift_attr.value.oid;
        break;
      default:
        break;
      }
    }

    sai_thrift_status_t sai_thrift_set_port_attribute(const sai_thrift_object_id_t port_id, const sai_thrift_attribute_t &thrift_attr) {
      printf("sai_thrift_set_port\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_port_api_t *port_api;
      status = sai_api_query(SAI_API_PORT, (void **) &port_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_object_id_t *buffer_profile_list = NULL;
      std::vector<sai_thrift_attribute_t> thrift_attr_list;
      thrift_attr_list.push_back(thrift_attr);
      sai_attribute_t attr;
      sai_thrift_parse_port_attributes(thrift_attr_list, &attr, &buffer_profile_list);
      status = port_api->set_port_attribute((sai_object_id_t)port_id, &attr);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to set port attributes.");
      }
      if (buffer_profile_list) free(buffer_profile_list);
      return status;
    }

    sai_thrift_status_t sai_thrift_set_router_interface_attribute(const sai_thrift_object_id_t rif_id, const sai_thrift_attribute_t &thrift_attr) {
      printf("sai_thrift_set_router_interface\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_router_interface_api_t *rif_api;
      status = sai_api_query(SAI_API_ROUTER_INTERFACE, (void **) &rif_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      std::vector<sai_thrift_attribute_t> thrift_attr_list;
      thrift_attr_list.push_back(thrift_attr);
      sai_attribute_t attr;
      sai_thrift_parse_router_interface_attributes(thrift_attr_list, &attr);
      status = rif_api->set_router_interface_attribute((sai_object_id_t)rif_id, &attr);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to set router interface attributes.");
      }
      return status;
    }

    sai_thrift_status_t sai_thrift_create_fdb_entry(const sai_thrift_fdb_entry_t& thrift_fdb_entry, const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      printf("sai_thrift_create_fdb_entry\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_fdb_api_t *fdb_api;
      sai_fdb_entry_t fdb_entry;
      status = sai_api_query(SAI_API_FDB, (void **) &fdb_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_thrift_parse_fdb_entry(thrift_fdb_entry, &fdb_entry);
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_fdb_attributes(thrift_attr_list, attr_list);
      uint32_t attr_count = thrift_attr_list.size();
      status = fdb_api->create_fdb_entry(&fdb_entry, attr_count, attr_list);
      free(attr_list);
      return status;
    }

    sai_thrift_status_t sai_thrift_delete_fdb_entry(const sai_thrift_fdb_entry_t& thrift_fdb_entry) {
      printf("sai_thrift_delete_fdb_entry\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_fdb_api_t *fdb_api;
      sai_fdb_entry_t fdb_entry;
      status = sai_api_query(SAI_API_FDB, (void **) &fdb_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_thrift_parse_fdb_entry(thrift_fdb_entry, &fdb_entry);
      status = fdb_api->remove_fdb_entry(&fdb_entry);
      return status;
    }

    sai_thrift_status_t sai_thrift_flush_fdb_entries(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      printf("sai_thrift_flush_fdb_entries\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_fdb_api_t *fdb_api;
      status = sai_api_query(SAI_API_FDB, (void **) &fdb_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_fdb_flush_attributes(thrift_attr_list, attr_list);
      uint32_t attr_count = thrift_attr_list.size();
      status = fdb_api->flush_fdb_entries(gSwitchId, attr_count, attr_list);
      free(attr_list);
      return status;
    }
    //listing all the fdb entries from map
    void sai_thrift_get_fdb_entries (sai_thrift_attribute_list_t& thrift_attr_list) {
      thrift_attr_list.attr_count = gFdbMap.size();

      sai_fdb_entry_t fdb_m;
      sai_object_id_t b_id;

      for (auto it = gFdbMap.begin(); it != gFdbMap.end(); it++) {
        fdb_m = it->first;
        b_id = it->second;

        sai_thrift_fdb_values_t fdb_value;
        fdb_value.bport_id=b_id;
        fdb_value.thrift_fdb_entry.bv_id=fdb_m.bv_id;
        fdb_value.thrift_fdb_entry.mac_address=mac_to_sai_thrift_string(fdb_m.mac_address);

        sai_thrift_attribute_t thrift_fdb_attributes;
        thrift_fdb_attributes.id = SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID;
        thrift_fdb_attributes.value.fdb_values = fdb_value;

        thrift_attr_list.attr_list.push_back(thrift_fdb_attributes);
      }
      return;
    }

    void sai_thrift_parse_vlan_attributes(const std_sai_thrift_attr_vctr_t &thrift_attr_list, sai_attribute_t *attr_list) {
      SAI_THRIFT_LOG_DBG("Called.");

      std_sai_thrift_attr_vctr_t::const_iterator cit = thrift_attr_list.begin();

      for (sai_uint32_t i = 0; i < thrift_attr_list.size(); i++, cit++) {
        sai_thrift_attribute_t attribute = *cit;
        attr_list[i].id = attribute.id;

        switch (attribute.id) {
        case SAI_VLAN_ATTR_VLAN_ID:
          attr_list[i].value.u16 = attribute.value.u16;
          break;
        case SAI_VLAN_ATTR_INGRESS_ACL:
          attr_list[i].value.oid = attribute.value.oid;
          break;

        default:
          SAI_THRIFT_LOG_ERR("Failed to parse VLAN attributes.");
          break;
        }
      }
    }

    void sai_thrift_parse_bridge_port_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;

        switch (attribute.id) {
        case SAI_BRIDGE_PORT_ATTR_TYPE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;

        case SAI_BRIDGE_PORT_ATTR_ADMIN_STATE:
          attr_list[i].value.booldata = attribute.value.booldata;
          break;

        case SAI_BRIDGE_PORT_ATTR_VLAN_ID:
          attr_list[i].value.u16 = attribute.value.u16;
          break;

        case SAI_BRIDGE_PORT_ATTR_PORT_ID:
        case SAI_BRIDGE_PORT_ATTR_RIF_ID:
        case SAI_BRIDGE_PORT_ATTR_TUNNEL_ID:
        case SAI_BRIDGE_PORT_ATTR_BRIDGE_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;

        default:
          SAI_THRIFT_LOG_ERR("Failed to parse Bridge Port attributes");
          break;
        }
      }
    }

    void sai_thrift_parse_bridge_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;

        switch (attribute.id) {
        case SAI_BRIDGE_ATTR_TYPE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;

        case SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES:
          attr_list[i].value.u32 = attribute.value.u32;
          break;

        case SAI_BRIDGE_ATTR_LEARN_DISABLE:
          attr_list[i].value.booldata = attribute.value.booldata;
          break;

        default:
          SAI_THRIFT_LOG_ERR("Failed to parse Bridge attributes.");
          break;
        }
      }
    }

    sai_thrift_object_id_t sai_thrift_create_vlan(const std_sai_thrift_attr_vctr_t &thrift_attr_list) {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_vlan_api_t *vlan_api = nullptr;
      auto status = sai_api_query(SAI_API_VLAN, reinterpret_cast<void**>(&vlan_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get VLAN API.");
        return SAI_NULL_OBJECT_ID;
      }

      sai_attribute_t *attr_list = nullptr;
      sai_uint32_t attr_size = thrift_attr_list.size();
      sai_thrift_alloc_attr(attr_list, attr_size);
      sai_thrift_parse_vlan_attributes(thrift_attr_list, attr_list);

      sai_object_id_t vlanObjId = 0;
      status = vlan_api->create_vlan(&vlanObjId, gSwitchId, attr_size, attr_list);
      sai_thrift_free_attr(attr_list);

      if (status == SAI_STATUS_SUCCESS) { return vlanObjId; }

      SAI_THRIFT_LOG_ERR("Failed to create VLAN.");

      return SAI_NULL_OBJECT_ID;
    }

    sai_thrift_status_t sai_thrift_remove_vlan(const sai_thrift_object_id_t vlan_oid) {
      printf("sai_thrift_delete_vlan\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_vlan_api_t *vlan_api;
      status = sai_api_query(SAI_API_VLAN, (void **) &vlan_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      status = vlan_api->remove_vlan(vlan_oid);
      return status;
    }

    void sai_thrift_get_vlan_stats(std::vector<int64_t> &thrift_counters,
        const sai_thrift_vlan_id_t vlan_id,
        const std::vector<sai_thrift_vlan_stat_counter_t> &thrift_counter_ids,
        const int32_t number_of_counters) {
      printf("sai_thrift_get_vlan_stats\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_vlan_api_t *vlan_api;
      status = sai_api_query(SAI_API_VLAN, (void **) &vlan_api);

      if (status != SAI_STATUS_SUCCESS) {
        return;
      }

      sai_vlan_stat_t *counter_ids = (sai_vlan_stat_t *) malloc(sizeof(sai_vlan_stat_t) * thrift_counter_ids.size());
      std::vector<int32_t>::const_iterator it = thrift_counter_ids.begin();
      uint64_t *counters = (uint64_t *) malloc(sizeof(uint64_t) * thrift_counter_ids.size());

      for (uint32_t i = 0; i < thrift_counter_ids.size(); i++, it++) {
        counter_ids[i] = (sai_vlan_stat_t) *it;
      }

      status = vlan_api->get_vlan_stats((sai_vlan_id_t) vlan_id,
          number_of_counters,
          (const sai_stat_id_t *)counter_ids,
          counters);

      for (uint32_t i = 0; i < thrift_counter_ids.size(); i++) { thrift_counters.push_back(counters[i]); }

      free(counter_ids);
      free(counters);

      return;
    }

    void sai_thrift_get_vlan_attribute(sai_thrift_attribute_list_t& thrift_attr_list, const sai_thrift_object_id_t vlan_id) {
      printf("sai_thrift_get_vlan_attribute\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_vlan_api_t *vlan_api;
      sai_attribute_t vlan_member_list_object_attribute;
      sai_thrift_attribute_t thrift_vlan_member_list_attribute;
      sai_object_list_t *vlan_member_list_object;
      status = sai_api_query(SAI_API_VLAN, (void **) &vlan_api);
      if (status != SAI_STATUS_SUCCESS) {
        return;
      }

      vlan_member_list_object_attribute.id = SAI_VLAN_ATTR_MEMBER_LIST;
      vlan_member_list_object_attribute.value.objlist.list = (sai_object_id_t *) malloc(sizeof(sai_object_id_t) * 128);
      vlan_member_list_object_attribute.value.objlist.count = 128;
      vlan_api->get_vlan_attribute(vlan_id, 1, &vlan_member_list_object_attribute);

      thrift_attr_list.attr_count = 1;
      std::vector<sai_thrift_attribute_t>& attr_list = thrift_attr_list.attr_list;
      thrift_vlan_member_list_attribute.id = SAI_VLAN_ATTR_MEMBER_LIST;
      thrift_vlan_member_list_attribute.value.objlist.count = vlan_member_list_object_attribute.value.objlist.count;
      std::vector<sai_thrift_object_id_t>& vlan_member_list = thrift_vlan_member_list_attribute.value.objlist.object_id_list;
      vlan_member_list_object = &vlan_member_list_object_attribute.value.objlist;
      for (uint32_t index = 0; index < vlan_member_list_object_attribute.value.objlist.count; index++) {
        vlan_member_list.push_back((sai_thrift_object_id_t) vlan_member_list_object->list[index]);
      }
      attr_list.push_back(thrift_vlan_member_list_attribute);
      free(vlan_member_list_object_attribute.value.objlist.list);
    }

    sai_thrift_status_t sai_thrift_set_vlan_attribute(const sai_thrift_object_id_t vlan_oid, const sai_thrift_attribute_t& thrift_attr)  {
      sai_status_t status;
      const std::vector<sai_thrift_attribute_t> thrift_attr_list = { thrift_attr };
      sai_vlan_api_t *vlan_api;
      sai_attribute_t *attr_list = nullptr;

      status = sai_api_query(SAI_API_VLAN, (void **) &vlan_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_thrift_alloc_attr(attr_list, 1);
      sai_thrift_parse_vlan_attributes(thrift_attr_list, attr_list);

      status = vlan_api->set_vlan_attribute(vlan_oid, attr_list);
      sai_thrift_free_attr(attr_list);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to set VLAN attribute");
        return status;
      }

      return status;
    }


    sai_thrift_object_id_t sai_thrift_create_vlan_member(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      printf("sai_thrift_create_vlan_member\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_vlan_api_t *vlan_api;
      sai_object_id_t vlan_member_id = 0;
      status = sai_api_query(SAI_API_VLAN, (void **) &vlan_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_vlan_member_attributes(thrift_attr_list, attr_list);
      uint32_t attr_count = thrift_attr_list.size();
      vlan_api->create_vlan_member(&vlan_member_id, gSwitchId, attr_count, attr_list);
      return vlan_member_id;
    }

    void sai_thrift_parse_vlan_member_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_VLAN_MEMBER_ATTR_VLAN_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        case SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        case SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        }
      }
    }

    void sai_thrift_get_vlan_member_attribute(sai_thrift_attribute_list_t& thrift_attr_list, const sai_thrift_object_id_t vlan_member_id) {
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_vlan_api_t *vlan_api;
      sai_attribute_t attr[3];

      SAI_THRIFT_FUNC_LOG();

      thrift_attr_list.attr_count = 0;

      status = sai_api_query(SAI_API_VLAN, (void **) &vlan_api);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to obtain vlan_api, status:%d", status);
        return;
      }

      attr[0].id = SAI_VLAN_MEMBER_ATTR_VLAN_ID;
      attr[1].id = SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID;
      attr[2].id = SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE;

      status = vlan_api->get_vlan_member_attribute(vlan_member_id, 3, attr);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to obtain vlan member attributes, status:%d", status);
        return;
      }

      sai_attributes_to_sai_thrift_list(attr, 3, thrift_attr_list.attr_list);
    }

    sai_thrift_status_t sai_thrift_remove_vlan_member(const sai_thrift_object_id_t vlan_member_id) {
      printf("sai_thrift_remove_vlan_member\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_vlan_api_t *vlan_api;
      status = sai_api_query(SAI_API_VLAN, (void **) &vlan_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      status = vlan_api->remove_vlan_member((sai_object_id_t) vlan_member_id);
      return status;
    }

    void sai_thrift_get_vlan_id(sai_thrift_result_t &ret, sai_thrift_object_id_t vlan_id) {
      sai_attribute_t vlan_attr;
      sai_vlan_api_t *vlan_api;

      SAI_THRIFT_FUNC_LOG();

      ret.status = sai_api_query(SAI_API_VLAN, (void **) &vlan_api);
      if (ret.status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to obtain vlan_api, status:%d", ret.status);
        return;
      }

      vlan_attr.id = SAI_VLAN_ATTR_VLAN_ID;
      ret.status = vlan_api->get_vlan_attribute((sai_object_id_t)vlan_id, 1, &vlan_attr);
      if (ret.status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to get vlan ID, status:%d", ret.status);
        return;
      }

      ret.data.u16 = vlan_attr.value.u16;
    }

    sai_thrift_object_id_t sai_thrift_create_virtual_router(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      printf("sai_thrift_create_virtual_router\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_virtual_router_api_t *vr_api;
      sai_object_id_t vr_id = 0;
      status = sai_api_query(SAI_API_VIRTUAL_ROUTER, (void **) &vr_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_vr_attributes(thrift_attr_list, attr_list);
      uint32_t attr_count = thrift_attr_list.size();
      vr_api->create_virtual_router(&vr_id, gSwitchId, attr_count, attr_list);
      free(attr_list);
      return vr_id;
    }

    sai_thrift_status_t sai_thrift_remove_virtual_router(const sai_thrift_object_id_t vr_id) {
      printf("sai_thrift_remove_virtual_router\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_virtual_router_api_t *vr_api;
      status = sai_api_query(SAI_API_VIRTUAL_ROUTER, (void **) &vr_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      status = vr_api->remove_virtual_router((sai_object_id_t)vr_id);
      return status;
    }

    sai_thrift_status_t sai_thrift_create_route(const sai_thrift_route_entry_t &thrift_route_entry, const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      printf("sai_thrift_create_route\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_route_api_t *route_api;
      sai_route_entry_t route_entry;
      status = sai_api_query(SAI_API_ROUTE, (void **) &route_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_thrift_parse_route_entry(thrift_route_entry, &route_entry);
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_route_attributes(thrift_attr_list, attr_list);
      uint32_t attr_count = thrift_attr_list.size();
      status = route_api->create_route_entry(&route_entry, attr_count, attr_list);
      free(attr_list);
      SAI_THRIFT_LOG_DBG("Exit.");
      return status;
    }

    sai_thrift_status_t sai_thrift_remove_route(const sai_thrift_route_entry_t &thrift_route_entry) {
      printf("sai_thrift_remove_route\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_route_api_t *route_api;
      sai_route_entry_t route_entry;
      status = sai_api_query(SAI_API_ROUTE, (void **) &route_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_thrift_parse_route_entry(thrift_route_entry, &route_entry);
      status = route_api->remove_route_entry(&route_entry);
      return status;
    }

    sai_thrift_object_id_t sai_thrift_create_router_interface(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      printf("sai_thrift_create_router_interface\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_router_interface_api_t *rif_api;
      sai_object_id_t rif_id = 0;
      status = sai_api_query(SAI_API_ROUTER_INTERFACE, (void **) &rif_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_router_interface_attributes(thrift_attr_list, attr_list);
      uint32_t attr_count = thrift_attr_list.size();
      status = rif_api->create_router_interface(&rif_id, gSwitchId, attr_count, attr_list);
      free(attr_list);
      return rif_id;
    }

    sai_thrift_status_t sai_thrift_remove_router_interface(const sai_thrift_object_id_t rif_id) {
      printf("sai_thrift_remove_router_interface\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_router_interface_api_t *rif_api;
      status = sai_api_query(SAI_API_ROUTER_INTERFACE, (void **) &rif_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      status = rif_api->remove_router_interface((sai_object_id_t)rif_id);
      return status;
    }

    sai_thrift_object_id_t sai_thrift_create_next_hop(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      printf("sai_thrift_create_next_hop\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_next_hop_api_t *nhop_api;
      sai_object_id_t nhop_id = 0;
      status = sai_api_query(SAI_API_NEXT_HOP, (void **) &nhop_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_next_hop_attributes(thrift_attr_list, attr_list);
      uint32_t attr_count = thrift_attr_list.size();
      status = nhop_api->create_next_hop(&nhop_id, gSwitchId, attr_count, attr_list);
      free(attr_list);
      return nhop_id;
    }

    sai_thrift_status_t sai_thrift_remove_next_hop(const sai_thrift_object_id_t next_hop_id) {
      printf("sai_thrift_remove_next_hop\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_next_hop_api_t *nhop_api;
      status = sai_api_query(SAI_API_NEXT_HOP, (void **) &nhop_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      status = nhop_api->remove_next_hop((sai_object_id_t)next_hop_id);
      return status;
    }

    sai_thrift_object_id_t sai_thrift_create_lag(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      printf("sai_thrift_create_lag\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_lag_api_t *lag_api;
      sai_object_id_t lag_id = 0;

      status = sai_api_query(SAI_API_LAG, (void **) &lag_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }

      status = lag_api->create_lag(&lag_id, gSwitchId, 0, nullptr);
      return lag_id;
    }

    sai_thrift_status_t sai_thrift_remove_lag(const sai_thrift_object_id_t lag_id) {
      printf("sai_thrift_remove_lag\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_lag_api_t *lag_api;
      status = sai_api_query(SAI_API_LAG, (void **) &lag_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      status = lag_api->remove_lag((sai_object_id_t)lag_id);
      return status;
    }

    sai_thrift_status_t sai_thrift_set_lag_attribute(const sai_thrift_object_id_t lag_id, const sai_thrift_attribute_t& thrift_attr) {
      sai_status_t status;
      const std::vector<sai_thrift_attribute_t> thrift_attr_list = { thrift_attr };
      sai_lag_api_t *lag_api;
      sai_attribute_t *attr_list = nullptr;

      status = sai_api_query(SAI_API_LAG, (void **) &lag_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }

      sai_thrift_alloc_attr(attr_list, 1);
      sai_thrift_parse_lag_attributes(thrift_attr_list, attr_list);

      status = lag_api->set_lag_attribute(lag_id, attr_list);
      sai_thrift_free_attr(attr_list);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to set LAG attribute");
        return status;
      }

      return status;
    }

    sai_thrift_object_id_t sai_thrift_create_lag_member(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      printf("sai_thrift_create_lag_member\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_lag_api_t *lag_api;
      sai_object_id_t lag_member_id;
      status = sai_api_query(SAI_API_LAG, (void **) &lag_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_lag_member_attributes(thrift_attr_list, attr_list);
      uint32_t attr_count = thrift_attr_list.size();
      status = lag_api->create_lag_member(&lag_member_id, gSwitchId, attr_count, attr_list);
      return lag_member_id;
    }

    sai_thrift_status_t sai_thrift_remove_lag_member(const sai_thrift_object_id_t lag_member_id) {
      printf("sai_thrift_remove_lag_member\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_lag_api_t *lag_api;
      status = sai_api_query(SAI_API_LAG, (void **) &lag_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      status = lag_api->remove_lag_member(lag_member_id);
      return status;
    }

    void sai_thrift_get_lag_member_attribute(sai_thrift_attribute_list_t& thrift_attr_list, const sai_thrift_object_id_t lag_member_id) {
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_attribute_t sai_attrs[2];
      sai_lag_api_t *lag_api;

      status = sai_api_query(SAI_API_LAG, (void **) &lag_api);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to obtain lag_api, status:%d", status);
        return;
      }

      SAI_THRIFT_FUNC_LOG();

      sai_attrs[0].id = SAI_LAG_MEMBER_ATTR_LAG_ID;
      sai_attrs[1].id = SAI_LAG_MEMBER_ATTR_PORT_ID;

      status = lag_api->get_lag_member_attribute(lag_member_id, 2, sai_attrs);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to obtain lag member attributes, status:%d", status);
        return;
      }

      sai_attributes_to_sai_thrift_list(sai_attrs, 2, thrift_attr_list.attr_list);
    }

    sai_thrift_object_id_t sai_thrift_create_stp_entry(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      printf("sai_thrift_create_stp\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_stp_api_t *stp_api;
      sai_vlan_id_t *vlan_list;
      sai_object_id_t stp_id;
      status = sai_api_query(SAI_API_STP, (void **) &stp_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_stp_attributes(thrift_attr_list, attr_list, &vlan_list);
      uint32_t attr_count = thrift_attr_list.size();
      status = (sai_object_id_t) stp_api->create_stp(&stp_id, gSwitchId, attr_count, attr_list);
      if (vlan_list) free(vlan_list);
      free(attr_list);
      return stp_id;
    }

    sai_thrift_status_t sai_thrift_remove_stp_entry(const sai_thrift_object_id_t stp_id) {
      printf("sai_thrift_remove_stp\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_stp_api_t *stp_api;
      status = sai_api_query(SAI_API_STP, (void **) &stp_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      status = (sai_thrift_status_t) stp_api->remove_stp(stp_id);
      return status;
    }

    sai_thrift_status_t sai_thrift_set_stp_port_state(const sai_thrift_object_id_t stp_id, const sai_thrift_object_id_t port_id, const sai_thrift_port_stp_port_state_t stp_port_state) {
      printf("sai_thrift_set_stp_port_state\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_stp_api_t *stp_api;
      status = sai_api_query(SAI_API_STP, (void **) &stp_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_attribute_t attr[1];
      std::memset(attr, '\0', sizeof(attr));
      attr[0].id = SAI_STP_PORT_ATTR_STATE;
      attr[0].value.s32 = stp_port_state;
      status = stp_api->set_stp_port_attribute(port_id, attr);
      return status;
    }

    sai_thrift_port_stp_port_state_t sai_thrift_get_stp_port_state(const sai_thrift_object_id_t stp_id, const sai_thrift_object_id_t port_id) {
      printf("sai_thrift_get_stp_port_state\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_stp_api_t *stp_api;
      status = sai_api_query(SAI_API_STP, (void **) &stp_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_attribute_t attr[1];
      std::memset(attr, '\0', sizeof(attr));
      attr[0].id = SAI_STP_PORT_ATTR_STATE;
      status = stp_api->get_stp_port_attribute(port_id, 1, attr);
      return (sai_thrift_port_stp_port_state_t) attr[0].value.s32;
    }

    sai_thrift_status_t sai_thrift_create_neighbor_entry(const sai_thrift_neighbor_entry_t& thrift_neighbor_entry, const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      printf("sai_thrift_create_neighbor_entry\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_neighbor_api_t *neighbor_api;
      status = sai_api_query(SAI_API_NEIGHBOR, (void **) &neighbor_api);
      sai_neighbor_entry_t neighbor_entry;
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_thrift_parse_neighbor_entry(thrift_neighbor_entry, &neighbor_entry);
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_neighbor_attributes(thrift_attr_list, attr_list);
      uint32_t attr_count = thrift_attr_list.size();
      status = neighbor_api->create_neighbor_entry(&neighbor_entry, attr_count, attr_list);
      free(attr_list);
      return status;
    }

    sai_thrift_status_t sai_thrift_remove_neighbor_entry(const sai_thrift_neighbor_entry_t& thrift_neighbor_entry) {
      printf("sai_thrift_remove_neighbor_entry\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_neighbor_api_t *neighbor_api;
      sai_neighbor_entry_t neighbor_entry;
      status = sai_api_query(SAI_API_NEIGHBOR, (void **) &neighbor_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_thrift_parse_neighbor_entry(thrift_neighbor_entry, &neighbor_entry);
      status = neighbor_api->remove_neighbor_entry(&neighbor_entry);
      return status;
    }

    sai_thrift_status_t sai_thrift_set_neighbor_entry_attribute(const sai_thrift_neighbor_entry_t& thrift_neighbor_entry, const std::vector<sai_thrift_attribute_t> & thrift_attr) {
      printf("sai_thrift_set_neighbor_entry_attribute\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_neighbor_api_t *neighbor_api;
      status = sai_api_query(SAI_API_NEIGHBOR, (void **) &neighbor_api);
      sai_neighbor_entry_t neighbor_entry;
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_thrift_parse_neighbor_entry(thrift_neighbor_entry, &neighbor_entry);
      sai_attribute_t *attr= (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr.size());
      sai_thrift_parse_neighbor_attributes(thrift_attr, attr);
      status = neighbor_api->set_neighbor_entry_attribute(&neighbor_entry, attr);
      free(attr);
      return status;
    }

    sai_thrift_object_id_t sai_thrift_get_cpu_port_id() {
      sai_status_t status;
      sai_attribute_t attr;
      sai_switch_api_t *switch_api;
      sai_thrift_object_id_t cpu_port_id;
      const char* f_name = __FUNCTION__;
      printf("%s\n", f_name);
      status = sai_api_query(SAI_API_SWITCH, (void **) &switch_api);
      if (status != SAI_STATUS_SUCCESS) {
        printf("%s failed to obtain switch_api, status:%d\n", f_name, status);
        return SAI_NULL_OBJECT_ID;
      }
      attr.id = SAI_SWITCH_ATTR_CPU_PORT;
      status = switch_api->get_switch_attribute(gSwitchId, 1, &attr);
      if (status != SAI_STATUS_SUCCESS) {
        printf("%s failed, status:%d\n", f_name, status);
        return SAI_NULL_OBJECT_ID;
      }
      cpu_port_id = (sai_thrift_object_id_t) attr.value.oid;
      return cpu_port_id;
    }

    sai_thrift_object_id_t sai_thrift_get_default_router_id() {
      sai_status_t status;
      sai_attribute_t attr;
      sai_switch_api_t *switch_api;
      sai_thrift_object_id_t default_router_id;
      const char* f_name = __FUNCTION__;
      printf("%s\n", f_name);
      status = sai_api_query(SAI_API_SWITCH, (void **) &switch_api);
      if (status != SAI_STATUS_SUCCESS) {
        printf("%s failed to obtain switch_api, status:%d\n", f_name, status);
        return SAI_NULL_OBJECT_ID;
      }
      attr.id = SAI_SWITCH_ATTR_DEFAULT_VIRTUAL_ROUTER_ID;
      status = switch_api->get_switch_attribute(gSwitchId, 1, &attr);
      if (status != SAI_STATUS_SUCCESS) {
        printf("%s. Failed to get switch virtual router ID, status %d", f_name, status);
        return SAI_NULL_OBJECT_ID;
      }
      default_router_id = (sai_thrift_object_id_t)attr.value.oid;
      return default_router_id;
    }

    sai_thrift_object_id_t sai_thrift_get_default_1q_bridge_id() {
      sai_switch_api_t *switch_api;
      sai_attribute_t attr;
      sai_status_t status;

      SAI_THRIFT_FUNC_LOG();

      status = sai_api_query(SAI_API_SWITCH, (void **) &switch_api);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to obtain switch_api, status:%d\n", status);
        return SAI_NULL_OBJECT_ID;
      }

      attr.id = SAI_SWITCH_ATTR_DEFAULT_1Q_BRIDGE_ID;
      status = switch_api->get_switch_attribute(gSwitchId, 1, &attr);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get switch virtual router ID, status %d", status);
        return SAI_NULL_OBJECT_ID;
      }

      return (sai_thrift_object_id_t)attr.value.oid;
    }

    void sai_thrift_get_default_vlan_id(sai_thrift_result_t &ret) {
      sai_switch_api_t *switch_api;
      sai_attribute_t attr;

      SAI_THRIFT_FUNC_LOG();

      ret.status = sai_api_query(SAI_API_SWITCH, (void **) &switch_api);
      if (ret.status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to obtain switch_api, status:%d", ret.status);
        return;
      }

      attr.id = SAI_SWITCH_ATTR_DEFAULT_VLAN_ID;
      ret.status = switch_api->get_switch_attribute(gSwitchId, 1, &attr);
      if (ret.status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to get switch default vlan ID, status:%d", ret.status);
        return;
      }

      ret.data.oid = (sai_thrift_object_id_t)attr.value.oid;
    }

    sai_thrift_object_id_t sai_thrift_get_default_trap_group() {
      sai_status_t status;
      sai_attribute_t attr;
      sai_switch_api_t *switch_api;
      sai_thrift_object_id_t default_trap_group;
      const char* f_name = __FUNCTION__;
      printf("%s\n", f_name);
      status = sai_api_query(SAI_API_SWITCH, (void **) &switch_api);
      if (status != SAI_STATUS_SUCCESS) {
        printf("%s failed to obtain switch_api, status:%d\n", f_name, status);
        return SAI_NULL_OBJECT_ID;
      }
      attr.id = SAI_SWITCH_ATTR_DEFAULT_TRAP_GROUP;
      status = switch_api->get_switch_attribute(gSwitchId, 1, &attr);
      if (status != SAI_STATUS_SUCCESS) {
        printf("%s. Failed to get switch default trap group, status %d", f_name, status);
        return SAI_NULL_OBJECT_ID;
      }
      default_trap_group = (sai_thrift_object_id_t)attr.value.oid;
      return default_trap_group;
    }

    void sai_thrift_get_switch_attribute(sai_thrift_attribute_list_t& thrift_attr_list) {
      printf("sai_thrift_get_switch_attribute\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_switch_api_t *switch_api;
      sai_attribute_t max_port_attribute;
      sai_attribute_t port_list_object_attribute;
      sai_thrift_attribute_t thrift_port_list_attribute;
      sai_object_list_t *port_list_object;
      int max_ports = 0;
      status = sai_api_query(SAI_API_SWITCH, (void **) &switch_api);
      if (status != SAI_STATUS_SUCCESS) {
        printf("sai_api_query failed!!!\n");
        return;
      }

      max_port_attribute.id = SAI_SWITCH_ATTR_PORT_NUMBER;
      switch_api->get_switch_attribute(gSwitchId, 1, &max_port_attribute);
      max_ports = max_port_attribute.value.u32;
      port_list_object_attribute.id = SAI_SWITCH_ATTR_PORT_LIST;
      port_list_object_attribute.value.objlist.list = (sai_object_id_t *) malloc(sizeof(sai_object_id_t) * max_ports);
      port_list_object_attribute.value.objlist.count = max_ports;
      switch_api->get_switch_attribute(gSwitchId, 1, &port_list_object_attribute);

      thrift_attr_list.attr_count = 1;
      std::vector<sai_thrift_attribute_t>& attr_list = thrift_attr_list.attr_list;
      thrift_port_list_attribute.id = SAI_SWITCH_ATTR_PORT_LIST;
      thrift_port_list_attribute.value.objlist.count = max_ports;
      std::vector<sai_thrift_object_id_t>& port_list = thrift_port_list_attribute.value.objlist.object_id_list;
      port_list_object = &port_list_object_attribute.value.objlist;
      for (int index = 0; index < max_ports; index++) {
        port_list.push_back((sai_thrift_object_id_t) port_list_object->list[index]);
      }
      attr_list.push_back(thrift_port_list_attribute);
      free(port_list_object_attribute.value.objlist.list);
    }

    sai_thrift_status_t sai_thrift_set_switch_attribute(const sai_thrift_attribute_t& thrift_attr) {
      printf("sai_thrift_set_switch_attribute\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_switch_api_t *switch_api;
      sai_attribute_t attr;
      status = sai_api_query(SAI_API_SWITCH, (void **) &switch_api);
      if (status != SAI_STATUS_SUCCESS) {
        printf("sai_api_query failed!!!\n");
        return status;
      }

      sai_thrift_parse_switch_attribute(thrift_attr, &attr);

      status = switch_api->set_switch_attribute(gSwitchId, &attr);
      return status;
    }

    void sai_thrift_parse_switch_attribute(const sai_thrift_attribute_t &thrift_attr, sai_attribute_t *attr) {
      attr->id = thrift_attr.id;

      switch (thrift_attr.id) {
      case SAI_SWITCH_ATTR_SRC_MAC_ADDRESS:
        sai_thrift_string_to_mac(thrift_attr.value.mac, attr->value.mac);
        break;

      case SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION:
      case SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION:
      case SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION:
        attr->value.s32 = thrift_attr.value.s32;
        break;
      case SAI_SWITCH_ATTR_FDB_AGING_TIME:
        attr->value.u32 = thrift_attr.value.u32;
        break;

      case SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_SEED:
        attr->value.u32 = thrift_attr.value.u32;
        break;

      case SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_SEED:
        attr->value.u32 = thrift_attr.value.u32;
        break;

      default:
        printf("unknown thrift_attr id: %d\n", thrift_attr.id);
      }
    }

    void sai_thrift_get_port_list_by_front_port(sai_thrift_attribute_t& thrift_attr) {
      printf("sai_thrift_get_port_list_by_front_port\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_switch_api_t *switch_api;
      sai_port_api_t *port_api;
      sai_attribute_t max_port_attribute;
      sai_attribute_t port_list_object_attribute;
      sai_attribute_t port_lane_list_attribute;
      sai_thrift_attribute_t thrift_port_list_attribute;
      int max_ports = 0;
      extern std::map<std::set<int>, std::string> gPortMap;
      std::map<std::set<int>, std::string>::iterator gPortMapIt;

      status = sai_api_query(SAI_API_SWITCH, (void **) &switch_api);
      if (status != SAI_STATUS_SUCCESS) {
        printf("sai_api_query failed!!!\n");
        return;
      }

      status = sai_api_query(SAI_API_PORT, (void **) &port_api);
      if (status != SAI_STATUS_SUCCESS) {
        printf("sai_api_query failed!!!\n");
        return;
      }

      max_port_attribute.id = SAI_SWITCH_ATTR_PORT_NUMBER;
      switch_api->get_switch_attribute(gSwitchId, 1, &max_port_attribute);
      max_ports = max_port_attribute.value.u32;
      port_list_object_attribute.id = SAI_SWITCH_ATTR_PORT_LIST;
      port_list_object_attribute.value.objlist.list = (sai_object_id_t *) malloc(sizeof(sai_object_id_t) * max_ports);
      port_list_object_attribute.value.objlist.count = max_ports;
      switch_api->get_switch_attribute(gSwitchId, 1, &port_list_object_attribute);
      std::map<int, sai_object_id_t> front_to_sai_map;

      for (int i=0 ; i<max_ports ; i++) {
        port_lane_list_attribute.id = SAI_PORT_ATTR_HW_LANE_LIST;
        port_lane_list_attribute.value.u32list.list = (uint32_t *) malloc(sizeof(uint32_t) * 8);
        port_lane_list_attribute.value.u32list.count = 8;
        port_api->get_port_attribute(port_list_object_attribute.value.objlist.list[i], 1, &port_lane_list_attribute);

        uint32_t laneCnt = port_lane_list_attribute.value.u32list.count;
        uint32_t laneMatchCount = 0;

        for (gPortMapIt = gPortMap.begin(); gPortMapIt != gPortMap.end(); gPortMapIt++) {
          laneMatchCount = 0;
          for (uint32_t j=0; j<laneCnt; j++) {
            if (gPortMapIt->first.count(port_lane_list_attribute.value.u32list.list[j])) {
              laneMatchCount++;
            } else {
              break;
            }
          }
          if (laneMatchCount == laneCnt) {
            break;
          }
        }

        if (gPortMapIt != gPortMap.end()) {
          std::string front_port_alias = gPortMapIt->second.c_str();
          std::string front_port_number;
          int front_num_to_sort=0;
          for (size_t k=0 ; k<front_port_alias.length() ; k++) {
            if (front_port_alias[k] >= '0' && front_port_alias[k] <= '9') {
              front_port_number.push_back(front_port_alias[k]);
            }
          }
          front_num_to_sort = std::stoi(front_port_number);
          front_to_sai_map.insert(std::pair<int,sai_object_id_t>(front_num_to_sort,port_list_object_attribute.value.objlist.list[i]));
        }
        else {
          printf("DIDN'T FOUND FRONT PORT FOR LANE SET\n");
        }
        free(port_lane_list_attribute.value.u32list.list);
      }

      sai_thrift_attribute_t& attr = thrift_attr;
      thrift_port_list_attribute.id = SAI_SWITCH_ATTR_PORT_LIST;
      thrift_port_list_attribute.value.objlist.count = max_ports;
      std::vector<sai_thrift_object_id_t>& port_list = thrift_port_list_attribute.value.objlist.object_id_list;
      for (std::map<int, sai_object_id_t>::iterator it = front_to_sai_map.begin() ; it != front_to_sai_map.end(); it++) {
        port_list.push_back((sai_thrift_object_id_t) it->second);
      }
      attr = thrift_port_list_attribute;
      free(port_list_object_attribute.value.objlist.list);
    }

    sai_thrift_object_id_t sai_thrift_get_port_id_by_front_port(const std::string& port_name) {
      printf("sai_thrift_get_port_id_by_front_port\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_switch_api_t *switch_api;
      sai_port_api_t *port_api;
      sai_attribute_t max_port_attribute;
      sai_attribute_t port_list_object_attribute;
      sai_attribute_t port_lane_list_attribute;
      int max_ports = 0;
      sai_thrift_object_id_t port_id;
      extern std::map<std::set<int>, std::string> gPortMap;
      std::map<std::set<int>, std::string>::iterator gPortMapIt;

      status = sai_api_query(SAI_API_SWITCH, (void **) &switch_api);
      if (status != SAI_STATUS_SUCCESS) {
        printf("sai_api_query failed!!!\n");
        return SAI_NULL_OBJECT_ID;
      }
      status = sai_api_query(SAI_API_PORT, (void **) &port_api);
      if (status != SAI_STATUS_SUCCESS) {
        printf("sai_api_query failed!!!\n");
        return SAI_NULL_OBJECT_ID;
      }
      for (gPortMapIt = gPortMap.begin() ; gPortMapIt != gPortMap.end() ; gPortMapIt++) {
        if (gPortMapIt->second == port_name) {
          break;
        }
      }

      std::set<int> lane_set;
      if (gPortMapIt != gPortMap.end()) {
        lane_set = gPortMapIt->first;
      }
      else {
        printf("Didn't find matching port to received name!\n");
        return SAI_NULL_OBJECT_ID;
      }

      max_port_attribute.id = SAI_SWITCH_ATTR_PORT_NUMBER;
      switch_api->get_switch_attribute(gSwitchId, 1, &max_port_attribute);
      max_ports = max_port_attribute.value.u32;
      port_list_object_attribute.id = SAI_SWITCH_ATTR_PORT_LIST;
      port_list_object_attribute.value.objlist.list = (sai_object_id_t *) malloc(sizeof(sai_object_id_t) * max_ports);
      port_list_object_attribute.value.objlist.count = max_ports;
      switch_api->get_switch_attribute(gSwitchId, 1, &port_list_object_attribute);

      for (int i=0 ; i<max_ports ; i++) {
        port_lane_list_attribute.id = SAI_PORT_ATTR_HW_LANE_LIST;
        port_lane_list_attribute.value.u32list.list = (uint32_t *) malloc(sizeof(uint32_t) * 8);
        port_lane_list_attribute.value.u32list.count = 8;
        port_api->get_port_attribute(port_list_object_attribute.value.objlist.list[i], 1, &port_lane_list_attribute);

        uint32_t laneCnt = port_lane_list_attribute.value.u32list.count;
        uint32_t laneMatchCount = 0;
        for (uint32_t j=0 ; j<laneCnt; j++) {
          if (lane_set.count(port_lane_list_attribute.value.u32list.list[j])) {
            laneMatchCount++;
          } else {
            break;
          }
        }
        if (laneCnt == laneMatchCount) {
          port_id = (sai_thrift_object_id_t) port_list_object_attribute.value.objlist.list[i];
          free(port_list_object_attribute.value.objlist.list);
          free(port_lane_list_attribute.value.u32list.list);
          return port_id;
        }
        free(port_lane_list_attribute.value.u32list.list);
      }
      printf("Didn't find port\n");
      free(port_list_object_attribute.value.objlist.list);
      return SAI_NULL_OBJECT_ID;
    }


    void sai_thrift_create_bridge_port(sai_thrift_result_t &ret, const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      sai_bridge_api_t *bridge_api;
      sai_attribute_t *sai_attrs = nullptr;

      SAI_THRIFT_FUNC_LOG();

      ret.status = sai_api_query(SAI_API_BRIDGE, (void **) &bridge_api);
      if (ret.status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to obtain bridge_api, status:%d", ret.status);
        return;
      }

      sai_uint32_t attr_size = thrift_attr_list.size();

      sai_thrift_alloc_attr(sai_attrs, attr_size);

      sai_thrift_parse_bridge_port_attributes(thrift_attr_list, sai_attrs);

      ret.status = bridge_api->create_bridge_port((sai_object_id_t *) &ret.data.oid, gSwitchId, attr_size, sai_attrs);
      if (ret.status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to create bridge port, status:%d", ret.status);
      }

      sai_thrift_free_attr(sai_attrs);
    }

    sai_thrift_status_t sai_thrift_remove_bridge_port(const sai_thrift_object_id_t bridge_port_id) {
      sai_bridge_api_t *bridge_api;
      sai_status_t status;

      SAI_THRIFT_FUNC_LOG();

      status = sai_api_query(SAI_API_BRIDGE, (void **) &bridge_api);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to obtain bridge_api, status:%d", status);
        return status;
      }

      return bridge_api->remove_bridge_port((sai_object_id_t) bridge_port_id);
    }

    void sai_thrift_get_bridge_port_list(sai_thrift_result_t &ret, sai_thrift_object_id_t bridge_id) {
      std::vector<sai_thrift_object_id_t>& port_list = ret.data.objlist.object_id_list;
      sai_bridge_api_t *bridge_api;
      uint32_t max_ports = 128;
      sai_attribute_t attr;

      SAI_THRIFT_FUNC_LOG();

      ret.status = sai_api_query(SAI_API_BRIDGE, (void **) &bridge_api);
      if (ret.status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to obtain bridge_api, status:%d", ret.status);
        return;
      }

      attr.id = SAI_BRIDGE_ATTR_PORT_LIST;
      attr.value.objlist.list = (sai_object_id_t *) calloc(max_ports, sizeof(sai_object_id_t));
      attr.value.objlist.count = max_ports;

      ret.status = bridge_api->get_bridge_attribute(bridge_id, 1, &attr);
      if (ret.status != SAI_STATUS_SUCCESS && attr.value.objlist.count > max_ports) {
        /* retry one more time with a bigger list */
        max_ports = attr.value.objlist.count;
        attr.value.objlist.list = (sai_object_id_t *) realloc(attr.value.objlist.list, max_ports * sizeof(sai_object_id_t));

        ret.status = bridge_api->get_bridge_attribute(bridge_id, 1, &attr);
      }

      if (ret.status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to obtain bridge ports list, status:%d", ret.status);
        free(attr.value.objlist.list);
        return;
      }

      for (uint32_t index = 0; index < attr.value.objlist.count; index++) {
        port_list.push_back((sai_thrift_object_id_t) attr.value.objlist.list[index]);
      }
      free(attr.value.objlist.list);
    }

    sai_thrift_status_t sai_thrift_set_bridge_port_attribute(const sai_thrift_object_id_t bridge_port_id,
        const sai_thrift_attribute_t& thrift_attr) {
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_bridge_api_t *bridge_api;
      sai_attribute_t attr;
      const std::vector<sai_thrift_attribute_t> thrift_attr_list = { thrift_attr };

      SAI_THRIFT_FUNC_LOG();

      status = sai_api_query(SAI_API_BRIDGE, (void **) &bridge_api);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to obtain bridge_api, status:%d", status);
        return status;
      }

      sai_thrift_parse_bridge_port_attributes(thrift_attr_list, &attr);

      return bridge_api->set_bridge_port_attribute(bridge_port_id, &attr);
    }

    void sai_thrift_get_bridge_port_attribute(sai_thrift_attribute_list_t& thrift_attr_list, const sai_thrift_object_id_t bridge_port_id) {
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_bridge_api_t *bridge_api;
      uint32_t attr_count = 0;
      sai_attribute_t attr[3];

      SAI_THRIFT_FUNC_LOG();

      thrift_attr_list.attr_count = 0;

      status = sai_api_query(SAI_API_BRIDGE, (void **) &bridge_api);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to obtain bridge_api, status:%d", status);
        return;
      }

      attr[0].id = SAI_BRIDGE_PORT_ATTR_TYPE;
      attr_count = 1;

      status = bridge_api->get_bridge_port_attribute(bridge_port_id, attr_count, attr);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to obtain bridge port type, status:%d", status);
        return;
      }

      sai_attributes_to_sai_thrift_list(attr, attr_count, thrift_attr_list.attr_list);

      switch (attr[0].value.s32) {
      case SAI_BRIDGE_PORT_TYPE_PORT:
        attr[0].id = SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_MODE;
        attr[1].id = SAI_BRIDGE_PORT_ATTR_PORT_ID;
        attr_count = 2;
        break;

      case SAI_BRIDGE_PORT_TYPE_TUNNEL:
        attr[0].id = SAI_BRIDGE_PORT_ATTR_TUNNEL_ID;
        attr_count = 1;
        break;

      default:
        return;
      }

      status = bridge_api->get_bridge_port_attribute(bridge_port_id, attr_count, attr);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to obtain bridge port attributes, status:%d", status);
        return;
      }

      sai_attributes_to_sai_thrift_list(attr, attr_count, thrift_attr_list.attr_list);
    }

    void sai_thrift_create_bridge(sai_thrift_result_t &ret, const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      sai_bridge_api_t *bridge_api;
      sai_attribute_t  *sai_attrs = nullptr;

      SAI_THRIFT_FUNC_LOG();

      ret.status = sai_api_query(SAI_API_BRIDGE, (void **) &bridge_api);
      if (ret.status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to obtain bridge_api, status:%d", ret.status);
        return;
      }

      sai_uint32_t attr_size = thrift_attr_list.size();

      sai_thrift_alloc_attr(sai_attrs, attr_size);

      sai_thrift_parse_bridge_attributes(thrift_attr_list, sai_attrs);

      ret.status = bridge_api->create_bridge((sai_object_id_t *) &ret.data.oid, gSwitchId, attr_size, sai_attrs);
      if (ret.status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to create bridge, status:%d", ret.status);
      }

      sai_thrift_free_attr(sai_attrs);
    }

    sai_thrift_status_t sai_thrift_remove_bridge(const sai_thrift_object_id_t bridge_port_id) {
      sai_bridge_api_t *bridge_api;
      sai_status_t status;

      SAI_THRIFT_FUNC_LOG();

      status = sai_api_query(SAI_API_BRIDGE, (void **) &bridge_api);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("failed to obtain bridge_api, status:%d", status);
        return status;
      }

      return bridge_api->remove_bridge((sai_object_id_t) bridge_port_id);
    }

    sai_thrift_object_id_t sai_thrift_create_hostif (const std::vector<sai_thrift_attribute_t> &thrift_attr_list) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_hostif_api_t *hostif_api = nullptr;
      auto status = sai_api_query(SAI_API_HOSTIF, reinterpret_cast<void**>(&hostif_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return SAI_NULL_OBJECT_ID;
      }

      sai_attribute_t *attr_list = nullptr;
      sai_size_t attr_size = thrift_attr_list.size();
      sai_thrift_alloc_attr(attr_list, attr_size);
      sai_thrift_parse_hostif_attributes(attr_list, thrift_attr_list);

      sai_object_id_t hif_oid = 0;
      status = hostif_api->create_hostif (&hif_oid, gSwitchId, attr_size, attr_list);
      sai_thrift_free_attr(attr_list);

      if (status == SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_DBG("Exited.");
        return hif_oid;
      }

      SAI_THRIFT_LOG_ERR("Failed to create OID.");

      return SAI_NULL_OBJECT_ID;
    }

    sai_thrift_status_t sai_thrift_remove_hostif (const sai_thrift_object_id_t thrift_hif_id) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_hostif_api_t *hostif_api = nullptr;
      auto status = sai_api_query(SAI_API_HOSTIF, reinterpret_cast<void**>(&hostif_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return status;
      }

      status = hostif_api->remove_hostif (thrift_hif_id);

      if (status == SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_DBG("Exited.");
        return status;
      }

      SAI_THRIFT_LOG_ERR("Failed to remove OID.");
      return status;
    }

    sai_thrift_status_t sai_thrift_set_hostif_attribute(const sai_thrift_object_id_t thrift_hif_id, const sai_thrift_attribute_t &thrift_attr) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_hostif_api_t *hostif_api = nullptr;
      auto status = sai_api_query(SAI_API_HOSTIF, reinterpret_cast<void**>(&hostif_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return status;
      }

      const std::vector<sai_thrift_attribute_t> thrift_attr_list = { thrift_attr };

      sai_attribute_t *attr_list = nullptr;
      sai_size_t attr_size = thrift_attr_list.size();
      sai_thrift_alloc_attr(attr_list, attr_size);
      sai_thrift_parse_hostif_trap_group_attributes(attr_list, thrift_attr_list);

      status = hostif_api->set_hostif_attribute(thrift_hif_id, attr_list);
      sai_thrift_free_attr(attr_list);

      if (status == SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_DBG("Exited.");
        return status;
      }

      SAI_THRIFT_LOG_ERR("Failed to set attribute.");

      return status;
    }

    sai_thrift_object_id_t sai_thrift_create_hostif_table_entry(const std::vector<sai_thrift_attribute_t> &thrift_attr_list) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_hostif_api_t *hostif_api = nullptr;
      auto status = sai_api_query(SAI_API_HOSTIF, reinterpret_cast<void**>(&hostif_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return SAI_NULL_OBJECT_ID;
      }

      sai_attribute_t *attr_list = nullptr;
      sai_size_t attr_size = thrift_attr_list.size();
      sai_thrift_alloc_attr(attr_list, attr_size);
      sai_thrift_parse_hostif_table_entry_attributes(attr_list, thrift_attr_list);

      sai_object_id_t hif_table_entry_oid = 0;
      status = hostif_api->create_hostif_table_entry(&hif_table_entry_oid, gSwitchId, attr_size, attr_list);
      sai_thrift_free_attr(attr_list);

      if (status == SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_DBG("Exited.");
        return hif_table_entry_oid;
      }

      SAI_THRIFT_LOG_ERR("Failed to create OID.");

      return SAI_NULL_OBJECT_ID;
    }

    sai_thrift_status_t sai_thrift_remove_hostif_table_entry(const sai_thrift_object_id_t thrift_hif_table_entry_id) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_hostif_api_t *hostif_api = nullptr;
      auto status = sai_api_query(SAI_API_HOSTIF, reinterpret_cast<void**>(&hostif_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return status;
      }

      status = hostif_api->remove_hostif_table_entry(thrift_hif_table_entry_id);

      if (status == SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_DBG("Exited.");
        return status;
      }

      SAI_THRIFT_LOG_ERR("Failed to remove OID.");
      return status;
    }

    sai_thrift_status_t sai_thrift_set_hostif_table_entry_attribute(const sai_thrift_object_id_t thrift_hif_table_entry_id, const sai_thrift_attribute_t &thrift_attr) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_hostif_api_t *hostif_api = nullptr;
      auto status = sai_api_query(SAI_API_HOSTIF, reinterpret_cast<void**>(&hostif_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return status;
      }

      const std::vector<sai_thrift_attribute_t> thrift_attr_list = { thrift_attr };

      sai_attribute_t *attr_list = nullptr;
      sai_size_t attr_size = thrift_attr_list.size();
      sai_thrift_alloc_attr(attr_list, attr_size);
      sai_thrift_parse_hostif_trap_group_attributes(attr_list, thrift_attr_list);

      status = hostif_api->set_hostif_table_entry_attribute(thrift_hif_table_entry_id, attr_list);
      sai_thrift_free_attr(attr_list);

      if (status == SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_DBG("Exited.");
        return status;
      }

      SAI_THRIFT_LOG_ERR("Failed to set attribute.");
      return status;
    }

    sai_thrift_object_id_t sai_thrift_create_hostif_trap_group(const std::vector<sai_thrift_attribute_t> &thrift_attr_list) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_hostif_api_t *hostif_api = nullptr;
      auto status = sai_api_query(SAI_API_HOSTIF, reinterpret_cast<void**>(&hostif_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return SAI_NULL_OBJECT_ID;
      }

      sai_attribute_t *attr_list = nullptr;
      sai_size_t attr_size = thrift_attr_list.size();
      sai_thrift_alloc_attr(attr_list, attr_size);
      sai_thrift_parse_hostif_trap_group_attributes(attr_list, thrift_attr_list);

      sai_object_id_t hostif_trap_group_oid = 0;
      status = hostif_api->create_hostif_trap_group(&hostif_trap_group_oid, gSwitchId, attr_size, attr_list);
      sai_thrift_free_attr(attr_list);

      if (status == SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_DBG("Exited.");
        return hostif_trap_group_oid;
      }

      SAI_THRIFT_LOG_ERR("Failed to create OID.");

      return SAI_NULL_OBJECT_ID;
    }

    sai_thrift_status_t sai_thrift_remove_hostif_trap_group(const sai_thrift_object_id_t thrift_hostif_trap_group_id) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_hostif_api_t *hostif_api = nullptr;
      auto status = sai_api_query(SAI_API_HOSTIF, reinterpret_cast<void**>(&hostif_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return status;
      }

      status = hostif_api->remove_hostif_trap_group(thrift_hostif_trap_group_id);

      if (status == SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_DBG("Exited.");
        return status;
      }

      SAI_THRIFT_LOG_ERR("Failed to remove OID.");

      return status;
    }

    sai_thrift_status_t sai_thrift_set_hostif_trap_group_attribute(const sai_thrift_object_id_t thrift_hostif_trap_group_id,
        const sai_thrift_attribute_t &thrift_attr) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_hostif_api_t *hostif_api = nullptr;
      auto status = sai_api_query(SAI_API_HOSTIF, reinterpret_cast<void**>(&hostif_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return status;
      }

      const std::vector<sai_thrift_attribute_t> thrift_attr_list = { thrift_attr };

      sai_attribute_t *attr_list = nullptr;
      sai_size_t attr_size = thrift_attr_list.size();
      sai_thrift_alloc_attr(attr_list, attr_size);
      sai_thrift_parse_hostif_trap_group_attributes(attr_list, thrift_attr_list);

      status = hostif_api->set_hostif_trap_group_attribute(thrift_hostif_trap_group_id, attr_list);
      sai_thrift_free_attr(attr_list);

      if (status == SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_DBG("Exited.");
        return status;
      }

      SAI_THRIFT_LOG_ERR("Failed to set attribute.");

      return status;
    }

    sai_thrift_object_id_t sai_thrift_create_hostif_trap(const std::vector<sai_thrift_attribute_t> &thrift_attr_list) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_hostif_api_t *hostif_api = nullptr;
      auto status = sai_api_query(SAI_API_HOSTIF, reinterpret_cast<void**>(&hostif_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return SAI_NULL_OBJECT_ID;
      }

      sai_attribute_t *attr_list = nullptr;
      sai_size_t attr_size = thrift_attr_list.size();
      sai_thrift_alloc_attr(attr_list, attr_size);
      sai_thrift_parse_hostif_trap_attributes(attr_list, thrift_attr_list);

      sai_object_id_t hostif_trap_oid = 0;
      status = hostif_api->create_hostif_trap(&hostif_trap_oid, gSwitchId, attr_size, attr_list);
      sai_thrift_free_attr(attr_list);

      if (status == SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_DBG("Exited.");
        return hostif_trap_oid;
      }

      SAI_THRIFT_LOG_ERR("Failed to create OID.");

      return SAI_NULL_OBJECT_ID;
    }

    sai_thrift_status_t sai_thrift_remove_hostif_trap(const sai_thrift_object_id_t thrift_hostif_trap_id) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_hostif_api_t *hostif_api = nullptr;
      auto status = sai_api_query(SAI_API_HOSTIF, reinterpret_cast<void**>(&hostif_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return status;
      }

      status = hostif_api->remove_hostif_trap(thrift_hostif_trap_id);

      if (status == SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_DBG("Exited.");
        return status;
      }

      SAI_THRIFT_LOG_ERR("Failed to remove OID.");

      return status;
    }

    sai_thrift_status_t sai_thrift_set_hostif_trap_attribute(const sai_thrift_object_id_t thrift_hostif_trap_id, const sai_thrift_attribute_t &thrift_attr) {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_hostif_api_t *hostif_api = nullptr;
      auto status = sai_api_query(SAI_API_HOSTIF, reinterpret_cast<void**>(&hostif_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return status;
      }

      const std::vector<sai_thrift_attribute_t> thrift_attr_list = { thrift_attr };

      sai_attribute_t *attr_list = nullptr;
      sai_size_t attr_size = thrift_attr_list.size();
      sai_thrift_alloc_attr(attr_list, attr_size);
      sai_thrift_parse_hostif_trap_attributes(attr_list, thrift_attr_list);

      status = hostif_api->set_hostif_trap_attribute(thrift_hostif_trap_id, attr_list);
      sai_thrift_free_attr(attr_list);

      if (status == SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_DBG("Exited.");
        return status;
      }

      SAI_THRIFT_LOG_ERR("Failed to set attribute.");

      return status;
    }

    void sai_thrift_parse_acl_table_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_ACL_TABLE_ATTR_ACL_STAGE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        case SAI_ACL_TABLE_ATTR_ACL_BIND_POINT_TYPE_LIST:
          {
            int count = attribute.value.s32list.s32list.size();
            sai_int32_t *aclbp_list = NULL;
            std::vector<sai_int32_t>::const_iterator it = attribute.value.s32list.s32list.begin();
            aclbp_list = (sai_int32_t *) malloc(sizeof(sai_int32_t) * count);
            for (int j = 0; j < count; j++, it++) {
              *(aclbp_list + j) = (sai_int32_t) *it;
            }
            attr_list[i].value.s32list.list = aclbp_list;
            attr_list[i].value.s32list.count = count;
          }
          break;
        case SAI_ACL_TABLE_ATTR_FIELD_SRC_IPV6:
        case SAI_ACL_TABLE_ATTR_FIELD_DST_IPV6:
        case SAI_ACL_TABLE_ATTR_FIELD_SRC_MAC:
        case SAI_ACL_TABLE_ATTR_FIELD_DST_MAC:
        case SAI_ACL_TABLE_ATTR_FIELD_SRC_IP:
        case SAI_ACL_TABLE_ATTR_FIELD_DST_IP:
        case SAI_ACL_TABLE_ATTR_FIELD_IN_PORTS:
        case SAI_ACL_TABLE_ATTR_FIELD_OUT_PORTS:
        case SAI_ACL_TABLE_ATTR_FIELD_IN_PORT:
        case SAI_ACL_TABLE_ATTR_FIELD_OUT_PORT:
        case SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_ID:
        case SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_PRI:
        case SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_CFI:
        case SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_ID:
        case SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_PRI:
        case SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_CFI:
        case SAI_ACL_TABLE_ATTR_FIELD_L4_SRC_PORT:
        case SAI_ACL_TABLE_ATTR_FIELD_L4_DST_PORT:
        case SAI_ACL_TABLE_ATTR_FIELD_ETHER_TYPE:
        case SAI_ACL_TABLE_ATTR_FIELD_IP_PROTOCOL:
        case SAI_ACL_TABLE_ATTR_FIELD_DSCP:
        case SAI_ACL_TABLE_ATTR_FIELD_ECN:
        case SAI_ACL_TABLE_ATTR_FIELD_TTL:
        case SAI_ACL_TABLE_ATTR_FIELD_TOS:
        case SAI_ACL_TABLE_ATTR_FIELD_IP_FLAGS:
        case SAI_ACL_TABLE_ATTR_FIELD_TCP_FLAGS:
        case SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_TYPE:
        case SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_FRAG:
        case SAI_ACL_TABLE_ATTR_FIELD_IPV6_FLOW_LABEL:
        case SAI_ACL_TABLE_ATTR_FIELD_TC:
          attr_list[i].value.booldata = attribute.value.booldata;
          break;
        default:
          break;
        }
      }
    }

    void sai_thrift_parse_acl_entry_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list,
        sai_object_id_t **in_ports_list,
        sai_object_id_t **out_ports_list,
        sai_object_id_t **ingress_mirror_list,
        sai_object_id_t **egress_mirror_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_ACL_ENTRY_ATTR_TABLE_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        case SAI_ACL_ENTRY_ATTR_PRIORITY:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        case SAI_ACL_ENTRY_ATTR_ADMIN_STATE:
          attr_list[i].value.u8 = attribute.value.u8;
          break;
        case SAI_ACL_ENTRY_ATTR_FIELD_SRC_IPV6:
        case SAI_ACL_ENTRY_ATTR_FIELD_DST_IPV6:
          attr_list[i].value.aclfield.enable = attribute.value.aclfield.enable;
          sai_thrift_string_to_v6_ip(attribute.value.aclfield.data.ip6, attr_list[i].value.aclfield.data.ip6);
          sai_thrift_string_to_v6_ip(attribute.value.aclfield.mask.ip6, attr_list[i].value.aclfield.mask.ip6);
          break;
        case SAI_ACL_ENTRY_ATTR_FIELD_SRC_MAC:
        case SAI_ACL_ENTRY_ATTR_FIELD_DST_MAC:
          attr_list[i].value.aclfield.enable = attribute.value.aclfield.enable;
          sai_thrift_string_to_mac(attribute.value.aclfield.data.mac, attr_list[i].value.aclfield.data.mac);
          sai_thrift_string_to_mac(attribute.value.aclfield.mask.mac, attr_list[i].value.aclfield.mask.mac);
          break;
        case SAI_ACL_ENTRY_ATTR_FIELD_SRC_IP:
        case SAI_ACL_ENTRY_ATTR_FIELD_DST_IP:
          attr_list[i].value.aclfield.enable = attribute.value.aclfield.enable;
          sai_thrift_string_to_v4_ip(attribute.value.aclfield.data.ip4, &attr_list[i].value.aclfield.data.ip4);
          sai_thrift_string_to_v4_ip(attribute.value.aclfield.mask.ip4, &attr_list[i].value.aclfield.mask.ip4);
          break;
        case SAI_ACL_ENTRY_ATTR_FIELD_IN_PORT:
          attr_list[i].value.aclfield.enable   = attribute.value.aclfield.enable;
          attr_list[i].value.aclfield.data.oid = attribute.value.aclfield.data.oid;
          break;
        case SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS:
          {
            int count = attribute.value.aclfield.data.objlist.object_id_list.size();
            std::vector<sai_thrift_object_id_t>::const_iterator it = attribute.value.aclfield.data.objlist.object_id_list.begin();
            *in_ports_list = (sai_object_id_t *) malloc(sizeof(sai_object_id_t) * count);
            for (int j = 0; j < count; j++, it++) {
              (*in_ports_list)[j] = (sai_object_id_t) *it;
            }
            attr_list[i].value.aclfield.enable             = attribute.value.aclfield.enable;
            attr_list[i].value.aclfield.data.objlist.list  =  *in_ports_list;
            attr_list[i].value.aclfield.data.objlist.count =  count;
          }
          break;
        case SAI_ACL_ENTRY_ATTR_FIELD_OUT_PORT:
          attr_list[i].value.aclfield.enable   = attribute.value.aclfield.enable;
          attr_list[i].value.aclfield.data.oid = attribute.value.aclfield.data.oid;
          break;
        case SAI_ACL_ENTRY_ATTR_FIELD_OUT_PORTS:
          {
            int count = attribute.value.aclfield.data.objlist.object_id_list.size();
            std::vector<sai_thrift_object_id_t>::const_iterator it = attribute.value.aclfield.data.objlist.object_id_list.begin();
            *out_ports_list = (sai_object_id_t *) malloc(sizeof(sai_object_id_t) * count);
            for (int j = 0; j < count; j++, it++) {
              (*out_ports_list)[j] = (sai_object_id_t) *it;
            }
            attr_list[i].value.aclfield.enable             = attribute.value.aclfield.enable;
            attr_list[i].value.aclfield.data.objlist.list  =  *out_ports_list;
            attr_list[i].value.aclfield.data.objlist.count =  count;
          }
          break;
        case SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_PRI:
        case SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_CFI:
        case SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_PRI:
        case SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_CFI:
          break;
        case SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_ID:
        case SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_ID:
        case SAI_ACL_ENTRY_ATTR_FIELD_L4_SRC_PORT:
        case SAI_ACL_ENTRY_ATTR_FIELD_L4_DST_PORT:
        case SAI_ACL_ENTRY_ATTR_FIELD_ETHER_TYPE:
          attr_list[i].value.aclfield.enable   = attribute.value.aclfield.enable;
          attr_list[i].value.aclfield.data.u16 = attribute.value.aclfield.data.u16;
          attr_list[i].value.aclfield.mask.u16 = attribute.value.aclfield.mask.u16;
          break;
        case SAI_ACL_ENTRY_ATTR_FIELD_IP_PROTOCOL:
        case SAI_ACL_ENTRY_ATTR_FIELD_DSCP:
        case SAI_ACL_ENTRY_ATTR_FIELD_ECN:
        case SAI_ACL_ENTRY_ATTR_FIELD_TTL:
        case SAI_ACL_ENTRY_ATTR_FIELD_TOS:
        case SAI_ACL_ENTRY_ATTR_FIELD_IP_FLAGS:
        case SAI_ACL_ENTRY_ATTR_FIELD_TCP_FLAGS:
        case SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE:
        case SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_FRAG:
        case SAI_ACL_ENTRY_ATTR_FIELD_TC:
          attr_list[i].value.aclfield.enable  = attribute.value.aclfield.enable;
          attr_list[i].value.aclfield.data.u8 = attribute.value.aclfield.data.u8;
          attr_list[i].value.aclfield.mask.u8 = attribute.value.aclfield.mask.u8;
          break;
        case SAI_ACL_ENTRY_ATTR_FIELD_IPV6_FLOW_LABEL:
          attr_list[i].value.aclfield.enable   = attribute.value.aclfield.enable;
          attr_list[i].value.aclfield.data.u16 = attribute.value.aclfield.data.u16;
          attr_list[i].value.aclfield.mask.u16 = attribute.value.aclfield.mask.u16;
          break;
        case SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_INGRESS:
          {
            int count = attribute.value.aclaction.parameter.objlist.object_id_list.size();
            std::vector<sai_thrift_object_id_t>::const_iterator it = attribute.value.aclaction.parameter.objlist.object_id_list.begin();
            *ingress_mirror_list = (sai_object_id_t *) malloc(sizeof(sai_object_id_t) * count);
            for (int j = 0; j < count; j++, it++) {
              (*ingress_mirror_list)[j] = (sai_object_id_t) *it;
            }
            attr_list[i].value.aclaction.enable = attribute.value.aclaction.enable;
            attr_list[i].value.aclaction.parameter.objlist.list  =  *ingress_mirror_list;
            attr_list[i].value.aclaction.parameter.objlist.count =  count;
          }
          break;
        case SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_EGRESS:
          {
            int count = attribute.value.aclaction.parameter.objlist.object_id_list.size();
            std::vector<sai_thrift_object_id_t>::const_iterator it = attribute.value.aclaction.parameter.objlist.object_id_list.begin();
            *egress_mirror_list = (sai_object_id_t *) malloc(sizeof(sai_object_id_t) * count);
            for (int j = 0; j < count; j++, it++) {
              (*egress_mirror_list)[j] = (sai_object_id_t) *it;
            }
            attr_list[i].value.aclaction.enable = attribute.value.aclaction.enable;
            attr_list[i].value.aclaction.parameter.objlist.list  =  *egress_mirror_list;
            attr_list[i].value.aclaction.parameter.objlist.count =  count;
          }
          break;
        case SAI_ACL_ENTRY_ATTR_ACTION_SET_POLICER:
          attr_list[i].value.aclaction.enable        = attribute.value.aclaction.enable;
          attr_list[i].value.aclaction.parameter.oid = attribute.value.aclaction.parameter.oid;
          break;
        case SAI_ACL_ENTRY_ATTR_ACTION_COUNTER:
          attr_list[i].value.aclaction.enable        = attribute.value.aclaction.enable;
          attr_list[i].value.aclaction.parameter.oid = attribute.value.aclaction.parameter.oid;
          break;
        case SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION:
          attr_list[i].value.aclaction.enable        = attribute.value.aclaction.enable;
          attr_list[i].value.aclaction.parameter.u32 = attribute.value.aclaction.parameter.u32;
          break;
        default:
          break;
        }
      }
    }

    void sai_thrift_parse_acl_table_group_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_ACL_TABLE_GROUP_ATTR_ACL_STAGE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        case SAI_ACL_TABLE_GROUP_ATTR_ACL_BIND_POINT_TYPE_LIST:
          {
            int count = attribute.value.s32list.s32list.size();
            sai_int32_t *s32_list = NULL;
            std::vector<sai_int32_t>::const_iterator it = attribute.value.s32list.s32list.begin();
            s32_list = (sai_int32_t *) malloc(sizeof(sai_int32_t) * count);
            for (int j = 0; j < count; j++, it++) {
              *(s32_list + j) = (sai_int32_t) *it;
            }
            attr_list[i].value.s32list.list = s32_list;
            attr_list[i].value.s32list.count = count;
          }
          break;
        case SAI_ACL_TABLE_GROUP_ATTR_TYPE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        default:
          break;
        }
      }
    }

    void sai_thrift_parse_acl_table_group_member_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_GROUP_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        case SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        case SAI_ACL_TABLE_GROUP_MEMBER_ATTR_PRIORITY:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        default:
          break;
        }
      }
    }

    void sai_thrift_convert_to_acl_counter_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_ACL_COUNTER_ATTR_TABLE_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        case SAI_ACL_COUNTER_ATTR_ENABLE_PACKET_COUNT:
          attr_list[i].value.booldata = attribute.value.booldata;
          break;
        case SAI_ACL_COUNTER_ATTR_ENABLE_BYTE_COUNT:
          attr_list[i].value.booldata = attribute.value.booldata;
          break;
        case SAI_ACL_COUNTER_ATTR_PACKETS:
          attr_list[i].value.u64= attribute.value.u64;
          break;
        case SAI_ACL_COUNTER_ATTR_BYTES:
          attr_list[i].value.u64= attribute.value.u64;
          break;
        }
      }
    }

    void sai_thrift_convert_to_acl_thrift_counter_attributes(
        sai_attribute_t *attr_list,
        uint32_t attr_count,
        std::vector<sai_thrift_attribute_value_t> &thrift_attr_value_list) {
      sai_attribute_t attribute;
      sai_thrift_attribute_value_t thrift_attribute_value;
      for (uint32_t i = 0; i < attr_count; i++) {
        attribute = attr_list[i];
        switch (attribute.id) {
        case SAI_ACL_COUNTER_ATTR_TABLE_ID:
          thrift_attribute_value.oid = attribute.value.oid;
          break;
        case SAI_ACL_COUNTER_ATTR_ENABLE_PACKET_COUNT:
          thrift_attribute_value.booldata = attribute.value.booldata;
          break;
        case SAI_ACL_COUNTER_ATTR_ENABLE_BYTE_COUNT:
          thrift_attribute_value.booldata = attribute.value.booldata;
          break;
        case SAI_ACL_COUNTER_ATTR_PACKETS:
          thrift_attribute_value.u64= attribute.value.u64;
          break;
        case SAI_ACL_COUNTER_ATTR_BYTES:
          thrift_attribute_value.u64= attribute.value.u64;
          break;
        }
        thrift_attr_value_list.push_back(thrift_attribute_value);
      }
    }

    sai_thrift_object_id_t sai_thrift_create_acl_table(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      sai_object_id_t acl_table = 0ULL;
      sai_acl_api_t *acl_api;
      sai_status_t status = SAI_STATUS_SUCCESS;
      status = sai_api_query(SAI_API_ACL, (void **) &acl_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }

      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_acl_table_attributes(thrift_attr_list, attr_list);
      uint32_t attr_count = thrift_attr_list.size();
      status = acl_api->create_acl_table(&acl_table, gSwitchId, attr_count, attr_list);
      free(attr_list);
      return acl_table;
    }

    sai_thrift_status_t sai_thrift_remove_acl_table(const sai_thrift_object_id_t acl_table_id) {
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_acl_api_t *acl_api;
      status = sai_api_query(SAI_API_ACL, (void **) &acl_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      status = acl_api->remove_acl_table(acl_table_id);
      return status;
    }

    sai_thrift_object_id_t sai_thrift_create_acl_entry(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      sai_object_id_t acl_entry = 0ULL;
      sai_acl_api_t *acl_api;
      sai_status_t status = SAI_STATUS_SUCCESS;
      status = sai_api_query(SAI_API_ACL, (void **) &acl_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }

      sai_object_id_t *in_ports_list = NULL;
      sai_object_id_t *out_ports_list = NULL;
      sai_object_id_t *ingress_mirror_list = NULL;
      sai_object_id_t *egress_mirror_list = NULL;
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_acl_entry_attributes(thrift_attr_list, attr_list,
          &in_ports_list, &out_ports_list,
          &ingress_mirror_list, &egress_mirror_list);
      uint32_t attr_count = thrift_attr_list.size();
      status = acl_api->create_acl_entry(&acl_entry, gSwitchId, attr_count, attr_list);
      free(attr_list);
      if (in_ports_list) free(in_ports_list);
      if (out_ports_list) free(out_ports_list);
      if (ingress_mirror_list) free(ingress_mirror_list);
      if (egress_mirror_list) free(egress_mirror_list);
      return acl_entry;
    }

    sai_thrift_status_t sai_thrift_remove_acl_entry(const sai_thrift_object_id_t acl_entry) {
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_acl_api_t *acl_api;
      status = sai_api_query(SAI_API_ACL, (void **) &acl_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      status = acl_api->remove_acl_entry(acl_entry);
      return status;
    }

    sai_thrift_object_id_t sai_thrift_create_acl_table_group(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      sai_object_id_t acl_table_group_id = 0ULL;
      sai_acl_api_t *acl_api;
      sai_status_t status = SAI_STATUS_SUCCESS;
      status = sai_api_query(SAI_API_ACL, (void **) &acl_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }

      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_acl_table_group_attributes(thrift_attr_list, attr_list);
      uint32_t attr_count = thrift_attr_list.size();
      status = acl_api->create_acl_table_group(&acl_table_group_id, gSwitchId, attr_count, attr_list);
      free(attr_list);
      return acl_table_group_id;
    }

    sai_thrift_status_t sai_thrift_remove_acl_table_group(const sai_thrift_object_id_t acl_table_group_id) {
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_acl_api_t *acl_api;
      status = sai_api_query(SAI_API_ACL, (void **) &acl_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      status = acl_api->remove_acl_table_group(acl_table_group_id);
      return status;
    }

    sai_thrift_object_id_t sai_thrift_create_acl_table_group_member(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      sai_object_id_t acl_table_group_member_id = 0ULL;
      sai_acl_api_t *acl_api;
      sai_status_t status = SAI_STATUS_SUCCESS;
      status = sai_api_query(SAI_API_ACL, (void **) &acl_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }

      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_acl_table_group_member_attributes(thrift_attr_list, attr_list);
      uint32_t attr_count = thrift_attr_list.size();
      status = acl_api->create_acl_table_group_member(&acl_table_group_member_id, gSwitchId, attr_count, attr_list);
      free(attr_list);
      return acl_table_group_member_id;
    }

    sai_thrift_status_t sai_thrift_remove_acl_table_group_member(const sai_thrift_object_id_t acl_table_group_member_id) {
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_acl_api_t *acl_api;
      status = sai_api_query(SAI_API_ACL, (void **) &acl_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      status = acl_api->remove_acl_table_group_member(acl_table_group_member_id);
      return status;
    }

    sai_thrift_object_id_t sai_thrift_create_acl_counter(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      sai_object_id_t acl_counter_id = 0ULL;
      sai_acl_api_t *acl_api;
      sai_status_t status = SAI_STATUS_SUCCESS;
      status = sai_api_query(SAI_API_ACL, (void **) &acl_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_convert_to_acl_counter_attributes(thrift_attr_list, attr_list);
      uint32_t attr_count = thrift_attr_list.size();
      status = acl_api->create_acl_counter(&acl_counter_id, gSwitchId, attr_count, attr_list);
      free(attr_list);
      return acl_counter_id;
    }

    sai_thrift_status_t sai_thrift_remove_acl_counter(const sai_thrift_object_id_t acl_counter_id) {
      sai_acl_api_t *acl_api;
      sai_status_t status = SAI_STATUS_SUCCESS;
      status = sai_api_query(SAI_API_ACL, (void **) &acl_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      status = acl_api->remove_acl_counter(acl_counter_id);
      return status;
    }

    void sai_thrift_get_acl_counter_attribute(
        std::vector<sai_thrift_attribute_value_t> & thrift_attr_values,
        const sai_thrift_object_id_t acl_counter_id,
        const std::vector<int32_t> & thrift_attr_ids) {
      sai_acl_api_t *acl_api;
      sai_status_t status = SAI_STATUS_SUCCESS;
      status = sai_api_query(SAI_API_ACL, (void **) &acl_api);
      if (status != SAI_STATUS_SUCCESS) {
        return;
      }

      uint32_t attr_count = thrift_attr_ids.size();
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_ids.size());
      memset(attr_list, 0x0, sizeof(sizeof(sai_attribute_t) * thrift_attr_ids.size()));
      sai_thrift_parse_attribute_ids(thrift_attr_ids, attr_list);
      status = acl_api->get_acl_counter_attribute(acl_counter_id, attr_count, attr_list);
      if (status != SAI_STATUS_SUCCESS) {
        return;
      }

      sai_thrift_convert_to_acl_thrift_counter_attributes(
          attr_list,
          attr_count,
          thrift_attr_values);
      return;
    }

    void sai_thrift_parse_mirror_session_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_MIRROR_SESSION_ATTR_TYPE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        case SAI_MIRROR_SESSION_ATTR_MONITOR_PORT:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        case SAI_MIRROR_SESSION_ATTR_TC:
          attr_list[i].value.u8 = attribute.value.u8;
          break;
        case SAI_MIRROR_SESSION_ATTR_VLAN_TPID:
          attr_list[i].value.u16 = attribute.value.u32;
          break;
        case SAI_MIRROR_SESSION_ATTR_VLAN_ID:
          attr_list[i].value.u16 = attribute.value.u16;
          break;
        case SAI_MIRROR_SESSION_ATTR_VLAN_PRI:
          attr_list[i].value.u8 = attribute.value.u8;
          break;
        case SAI_MIRROR_SESSION_ATTR_VLAN_HEADER_VALID:
          attr_list[i].value.booldata = attribute.value.booldata;
          break;
        case SAI_MIRROR_SESSION_ATTR_ERSPAN_ENCAPSULATION_TYPE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        case SAI_MIRROR_SESSION_ATTR_IPHDR_VERSION:
          attr_list[i].value.u8 = attribute.value.u8;
          break;
        case SAI_MIRROR_SESSION_ATTR_TOS:
          attr_list[i].value.u8 = attribute.value.u16;
          break;
        case SAI_MIRROR_SESSION_ATTR_TTL:
          attr_list[i].value.u8 = attribute.value.u16;
          break;
        case SAI_MIRROR_SESSION_ATTR_SRC_IP_ADDRESS:
          sai_thrift_parse_ip_address(attribute.value.ipaddr, &attr_list[i].value.ipaddr);
          break;
        case SAI_MIRROR_SESSION_ATTR_DST_IP_ADDRESS:
          sai_thrift_parse_ip_address(attribute.value.ipaddr, &attr_list[i].value.ipaddr);
          break;
        case SAI_MIRROR_SESSION_ATTR_SRC_MAC_ADDRESS:
          sai_thrift_string_to_mac(attribute.value.mac, attr_list[i].value.mac);
          break;
        case SAI_MIRROR_SESSION_ATTR_DST_MAC_ADDRESS:
          sai_thrift_string_to_mac(attribute.value.mac, attr_list[i].value.mac);
          break;
        case SAI_MIRROR_SESSION_ATTR_GRE_PROTOCOL_TYPE:
          attr_list[i].value.u16 = attribute.value.u32;
          break;
        default:
          break;
        }
      }
    }

    sai_thrift_object_id_t sai_thrift_create_mirror_session(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      printf("sai_thrift_create_mirror_session\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_mirror_api_t *mirror_api;
      sai_object_id_t session_id = 0;
      status = sai_api_query(SAI_API_MIRROR, (void **) &mirror_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_mirror_session_attributes(thrift_attr_list, attr_list);
      uint32_t attr_count = thrift_attr_list.size();
      mirror_api->create_mirror_session(&session_id, gSwitchId, attr_count, attr_list);
      return session_id;
    }

    sai_thrift_status_t sai_thrift_remove_mirror_session(const sai_thrift_object_id_t session_id) {
      printf("sai_thrift_remove_mirror_session\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_mirror_api_t *mirror_api;
      status = sai_api_query(SAI_API_MIRROR, (void **) &mirror_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      status = mirror_api->remove_mirror_session((sai_object_id_t) session_id);
      return status;
    }

    sai_thrift_status_t sai_thrift_set_mirror_session_attribute(const sai_thrift_object_id_t session_id, const sai_thrift_attribute_t &thrift_attr) {
      printf("sai_thrift_set_mirror_session\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_mirror_api_t *mirror_api;
      status = sai_api_query(SAI_API_MIRROR, (void **) &mirror_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      std::vector<sai_thrift_attribute_t> thrift_attr_list;
      thrift_attr_list.push_back(thrift_attr);
      sai_attribute_t attr;
      sai_thrift_parse_mirror_session_attributes(thrift_attr_list, &attr);
      status = mirror_api->set_mirror_session_attribute((sai_object_id_t)session_id, &attr);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to set mirror session attributes.");
      }
      return status;
    }

    void sai_thrift_parse_policer_attributes(sai_attribute_t *attr_list,
        const std::vector<sai_thrift_attribute_t> &thrift_attr_list) const noexcept {
      if (attr_list == nullptr || thrift_attr_list.empty()) {
        SAI_THRIFT_LOG_ERR("Invalid input arguments.");
        return;
      }

      std::vector<sai_thrift_attribute_t>::const_iterator cit = thrift_attr_list.begin();

      for (sai_size_t i = 0; i < thrift_attr_list.size(); i++, cit++) {
        sai_thrift_attribute_t attribute = *cit;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_POLICER_ATTR_METER_TYPE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        case SAI_POLICER_ATTR_MODE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        case SAI_POLICER_ATTR_COLOR_SOURCE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        case SAI_POLICER_ATTR_CBS:
          attr_list[i].value.u64 = attribute.value.u64;
          break;
        case SAI_POLICER_ATTR_CIR:
          attr_list[i].value.u64 = attribute.value.u64;
          break;
        case SAI_POLICER_ATTR_PBS:
          attr_list[i].value.u64 = attribute.value.u64;
          break;
        case SAI_POLICER_ATTR_PIR:
          attr_list[i].value.u64 = attribute.value.u64;
          break;
        case SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        case SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        case SAI_POLICER_ATTR_RED_PACKET_ACTION:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        case SAI_POLICER_ATTR_ENABLE_COUNTER_PACKET_ACTION_LIST:
          for (sai_size_t j = 0; j < attribute.value.s32list.s32list.size(); j++) {
            attr_list[i].value.s32list.list[j] = attribute.value.s32list.s32list[j];
          }
          attr_list[i].value.s32list.count = attribute.value.s32list.s32list.size();
          break;
        default:
          SAI_THRIFT_LOG_ERR("Failed to parse attribute.");
          break;
        }
      }
    }

    sai_thrift_object_id_t sai_thrift_create_policer(const std::vector<sai_thrift_attribute_t> &thrift_attr_list) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_policer_api_t *policer_api = nullptr;
      auto status = sai_api_query(SAI_API_POLICER, reinterpret_cast<void**>(&policer_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return SAI_NULL_OBJECT_ID;
      }

      sai_attribute_t *attr_list = nullptr;
      sai_size_t attr_size = thrift_attr_list.size();

      sai_thrift_alloc_array(attr_list, attr_size);
      sai_thrift_parse_policer_attributes(attr_list, thrift_attr_list);

      sai_object_id_t policer_oid = 0;
      status = policer_api->create_policer(&policer_oid, gSwitchId, attr_size, attr_list);
      sai_thrift_free_array(attr_list);

      if (status == SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_DBG("Exited.");
        return policer_oid;
      }

      SAI_THRIFT_LOG_ERR("Failed to create OID.");

      return SAI_NULL_OBJECT_ID;
    }

    sai_thrift_status_t sai_thrift_remove_policer(const sai_thrift_object_id_t thrift_policer_id) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_policer_api_t *policer_api = nullptr;
      auto status = sai_api_query(SAI_API_POLICER, reinterpret_cast<void**>(&policer_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return status;
      }

      status = policer_api->remove_policer(thrift_policer_id);

      if (status == SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_DBG("Exited.");
        return status;
      }

      SAI_THRIFT_LOG_ERR("Failed to remove OID.");

      return status;
    }

    sai_thrift_status_t sai_thrift_set_policer_attribute(const sai_thrift_object_id_t thrift_policer_id, const sai_thrift_attribute_t &thrift_attr) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_policer_api_t *policer_api = nullptr;
      auto status = sai_api_query(SAI_API_POLICER, reinterpret_cast<void**>(&policer_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return status;
      }

      const std::vector<sai_thrift_attribute_t> thrift_attr_list = { thrift_attr };

      sai_attribute_t *attr_list = nullptr;
      sai_size_t attr_size = thrift_attr_list.size();

      sai_thrift_alloc_array(attr_list, attr_size);
      sai_thrift_parse_policer_attributes(attr_list, thrift_attr_list);

      status = policer_api->set_policer_attribute(thrift_policer_id, attr_list);
      sai_thrift_free_array(attr_list);

      if (status == SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_DBG("Exited.");
        return status;
      }

      SAI_THRIFT_LOG_ERR("Failed to set attribute.");

      return status;
    }

    void sai_thrift_get_policer_stats(std::vector<sai_thrift_uint64_t> &_return, const sai_thrift_object_id_t thrift_policer_id,
        const std::vector<sai_thrift_policer_stat_t> &thrift_counter_ids) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_policer_api_t *policer_api = nullptr;
      auto status = sai_api_query(SAI_API_POLICER, reinterpret_cast<void**>(&policer_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return;
      }

      auto counter_ids = reinterpret_cast<const sai_policer_stat_t*>(thrift_counter_ids.data());
      sai_size_t number_of_counters = thrift_counter_ids.size();
      sai_uint64_t *counters = nullptr;

      sai_thrift_alloc_array(counters, number_of_counters);

      status = policer_api->get_policer_stats(thrift_policer_id, number_of_counters, (const sai_stat_id_t *)counter_ids, counters);

      if (status == SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_DBG("Exited.");
        _return.assign(counters, counters + number_of_counters);
        sai_thrift_free_array(counters);
        return;
      }

      SAI_THRIFT_LOG_ERR("Failed to get statistics.");
      sai_thrift_free_array(counters);
    }

    sai_thrift_status_t sai_thrift_clear_policer_stats(const sai_thrift_object_id_t thrift_policer_id,
        const std::vector<sai_thrift_policer_stat_t> &thrift_counter_ids) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_policer_api_t *policer_api = nullptr;
      auto status = sai_api_query(SAI_API_POLICER, reinterpret_cast<void**>(&policer_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return status;
      }

      auto counter_ids = reinterpret_cast<const sai_policer_stat_t*>(thrift_counter_ids.data());
      sai_size_t number_of_counters = thrift_counter_ids.size();

      status = policer_api->clear_policer_stats(thrift_policer_id, number_of_counters, (const sai_stat_id_t *)counter_ids);

      if (status == SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_DBG("Exited.");
        return status;
      }

      SAI_THRIFT_LOG_ERR("Failed to clear statistics.");

      return status;
    }

    sai_thrift_object_id_t sai_thrift_create_scheduler_profile(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      printf("sai_thrift_create_scheduler_profile\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_scheduler_api_t *scheduler_api;
      sai_object_id_t scheduler_id = 0;
      status = sai_api_query(SAI_API_SCHEDULER, (void **) &scheduler_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_scheduler_attributes(thrift_attr_list, attr_list);
      uint32_t attr_count = thrift_attr_list.size();
      scheduler_api->create_scheduler(&scheduler_id, gSwitchId, attr_count, attr_list);
      free (attr_list);
      return scheduler_id;
    }

    sai_thrift_status_t sai_thrift_remove_scheduler_profile(const sai_thrift_object_id_t scheduler_id) {
      printf("sai_thrift_remove_scheduler\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_scheduler_api_t *scheduler_api;
      status = sai_api_query(SAI_API_SCHEDULER, (void **) &scheduler_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      status = scheduler_api->remove_scheduler((sai_object_id_t) scheduler_id);
      return status;
    }

    void sai_thrift_parse_scheduler_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT:
          attr_list[i].value.u8 = attribute.value.u8;
          break;
        case SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE:
          attr_list[i].value.u64 = attribute.value.u64;
          break;
        case SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE:
          attr_list[i].value.u64 = attribute.value.u64;
          break;
        case SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE :
          attr_list[i].value.u64 = attribute.value.u64;
          break;
        case SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE:
          attr_list[i].value.u64 = attribute.value.u64;
          break;
        case SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        }
      }
    }

    void sai_thrift_get_port_stats(std::vector<int64_t> & thrift_counters,
        const sai_thrift_object_id_t port_id,
        const std::vector<sai_thrift_port_stat_counter_t> & thrift_counter_ids,
        const int32_t number_of_counters) {
      printf("sai_thrift_get_port_stats\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_port_api_t *port_api;
      status = sai_api_query(SAI_API_PORT, (void **) &port_api);
      if (status != SAI_STATUS_SUCCESS) {
        return;
      }
      sai_port_stat_t *counter_ids = (sai_port_stat_t *) malloc(sizeof(sai_port_stat_t) * thrift_counter_ids.size());
      std::vector<int32_t>::const_iterator it = thrift_counter_ids.begin();
      uint64_t *counters = (uint64_t *) malloc(sizeof(uint64_t) * thrift_counter_ids.size());
      for (uint32_t i = 0; i < thrift_counter_ids.size(); i++, it++) {
        counter_ids[i] = (sai_port_stat_t) *it;
      }

      status = port_api->get_port_stats((sai_object_id_t) port_id,
          number_of_counters,
          (const sai_stat_id_t *)counter_ids,
          counters);

      for (uint32_t i = 0; i < thrift_counter_ids.size(); i++) {
        thrift_counters.push_back(counters[i]);
      }
      free(counter_ids);
      free(counters);
      return;
    }

    sai_thrift_status_t sai_thrift_clear_port_all_stats(const sai_thrift_object_id_t port_id) {
      printf("sai_thrift_clear_port_all_stats\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_port_api_t *port_api;
      status = sai_api_query(SAI_API_PORT, (void **) &port_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      status = port_api->clear_port_all_stats( (sai_object_id_t) port_id);
      return status;
    }

    void sai_thrift_get_port_attribute(sai_thrift_attribute_list_t& thrift_attr_list, const sai_thrift_object_id_t port_id) {
      printf("sai_thrift_get_port_attribute\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_port_api_t *port_api;
      sai_attribute_t max_queue_attribute;
      sai_attribute_t queue_list_object_attribute;
      sai_thrift_attribute_t thrift_queue_list_attribute;
      sai_object_list_t *queue_list_object;
      int max_queues = 0;
      status = sai_api_query(SAI_API_PORT, (void **) &port_api);
      if (status != SAI_STATUS_SUCCESS) {
        return;
      }

      max_queue_attribute.id = SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES;
      port_api->get_port_attribute(port_id, 1, &max_queue_attribute);
      max_queues = max_queue_attribute.value.u32;
      queue_list_object_attribute.id = SAI_PORT_ATTR_QOS_QUEUE_LIST;
      queue_list_object_attribute.value.objlist.list = (sai_object_id_t *) malloc(sizeof(sai_object_id_t) * max_queues);
      queue_list_object_attribute.value.objlist.count = max_queues;
      port_api->get_port_attribute(port_id, 1, &queue_list_object_attribute);

      std::vector<sai_thrift_attribute_t>& attr_list = thrift_attr_list.attr_list;
      thrift_queue_list_attribute.id = SAI_PORT_ATTR_QOS_QUEUE_LIST;
      thrift_queue_list_attribute.value.objlist.count = max_queues;
      std::vector<sai_thrift_object_id_t>& queue_list = thrift_queue_list_attribute.value.objlist.object_id_list;
      queue_list_object = &queue_list_object_attribute.value.objlist;
      for (int index = 0; index < max_queues; index++) {
        queue_list.push_back((sai_thrift_object_id_t) queue_list_object->list[index]);
      }
      attr_list.push_back(thrift_queue_list_attribute);
      free(queue_list_object_attribute.value.objlist.list);

      sai_attribute_t max_pg_attribute;
      sai_attribute_t pg_list_object_attribute;
      sai_thrift_attribute_t thrift_pg_list_attribute;
      sai_object_list_t *pg_list_object;
      int max_pg = 0;

      max_pg_attribute.id = SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS;
      port_api->get_port_attribute(port_id, 1, &max_pg_attribute);
      max_pg = max_pg_attribute.value.u32;
      pg_list_object_attribute.id = SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST;
      pg_list_object_attribute.value.objlist.list = (sai_object_id_t *) malloc(sizeof(sai_object_id_t) * max_pg);
      pg_list_object_attribute.value.objlist.count = max_pg;
      port_api->get_port_attribute(port_id, 1, &pg_list_object_attribute);

      thrift_pg_list_attribute.id = SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST;
      thrift_pg_list_attribute.value.objlist.count = max_pg;
      std::vector<sai_thrift_object_id_t>& pg_list = thrift_pg_list_attribute.value.objlist.object_id_list;
      pg_list_object = &pg_list_object_attribute.value.objlist;
      for (int index = 0; index < max_pg; index++) {
        pg_list.push_back((sai_thrift_object_id_t) pg_list_object->list[index]);
      }
      attr_list.push_back(thrift_pg_list_attribute);
      free(pg_list_object_attribute.value.objlist.list);

      sai_attribute_t port_hw_lane;
      sai_thrift_attribute_t thrift_port_hw_lane;
      sai_u32_list_t *lane_list_num;

      port_hw_lane.id = SAI_PORT_ATTR_HW_LANE_LIST;
      port_hw_lane.value.u32list.list = (uint32_t *) malloc(sizeof(uint32_t) * 8);
      port_hw_lane.value.u32list.count = 8;
      port_api->get_port_attribute(port_id, 1, &port_hw_lane);

      thrift_port_hw_lane.id = SAI_PORT_ATTR_HW_LANE_LIST;
      thrift_port_hw_lane.value.u32list.count = port_hw_lane.value.u32list.count;
      std::vector<int32_t>& lane_list = thrift_port_hw_lane.value.u32list.u32list;
      lane_list_num = &port_hw_lane.value.u32list;
      for (uint32_t index = 0; index < port_hw_lane.value.u32list.count ; index++) {
        lane_list.push_back((uint32_t) lane_list_num->list[index]);
      }
      attr_list.push_back(thrift_port_hw_lane);
      free(port_hw_lane.value.u32list.list);

      sai_attribute_t port_oper_status_attribute;
      sai_thrift_attribute_t thrift_port_status;
      port_oper_status_attribute.id = SAI_PORT_ATTR_OPER_STATUS;
      port_api->get_port_attribute(port_id, 1, &port_oper_status_attribute);

      thrift_port_status.id = SAI_PORT_ATTR_OPER_STATUS;
      thrift_port_status.value.s32 =  port_oper_status_attribute.value.s32;
      attr_list.push_back(thrift_port_status);

      sai_attribute_t port_mtu_status_attribute;
      sai_thrift_attribute_t thrift_port_mtu;
      port_mtu_status_attribute.id = SAI_PORT_ATTR_MTU;
      port_api->get_port_attribute(port_id, 1, &port_mtu_status_attribute);

      thrift_port_mtu.id = SAI_PORT_ATTR_MTU;
      thrift_port_mtu.value.u32 =  port_mtu_status_attribute.value.u32;
      attr_list.push_back(thrift_port_mtu);
    }

    void sai_thrift_get_queue_stats(std::vector<int64_t> & thrift_counters,
        const sai_thrift_object_id_t queue_id,
        const std::vector<sai_thrift_queue_stat_counter_t> & thrift_counter_ids,
        const int32_t number_of_counters) {
      printf("sai_thrift_get_queue_stats\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_queue_api_t *queue_api;
      status = sai_api_query(SAI_API_QUEUE, (void **) &queue_api);
      if (status != SAI_STATUS_SUCCESS) {
        return;
      }
      sai_queue_stat_t *counter_ids = (sai_queue_stat_t *) malloc(sizeof(sai_queue_stat_t) * thrift_counter_ids.size());
      std::vector<int32_t>::const_iterator it = thrift_counter_ids.begin();
      uint64_t *counters = (uint64_t *) malloc(sizeof(uint64_t) * thrift_counter_ids.size());
      for (uint32_t i = 0; i < thrift_counter_ids.size(); i++, it++) {
        counter_ids[i] = (sai_queue_stat_t) *it;
      }

      status = queue_api->get_queue_stats(
          (sai_object_id_t) queue_id,
          number_of_counters,
          (const sai_stat_id_t *)counter_ids,
          counters);

      for (uint32_t i = 0; i < thrift_counter_ids.size(); i++) {
        thrift_counters.push_back(counters[i]);
      }
      free(counter_ids);
      free(counters);
      return;
    }

    sai_thrift_status_t sai_thrift_set_queue_attribute(const sai_thrift_object_id_t queue_id,
        const sai_thrift_attribute_t& thrift_attr) {
      printf("sai_thrift_set_queue_attribute\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_queue_api_t *queue_api;
      status = sai_api_query(SAI_API_QUEUE, (void **) &queue_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_attribute_t attr;
      attr.id = thrift_attr.id;
      attr.value.oid = thrift_attr.value.oid;
      status = queue_api->set_queue_attribute((sai_object_id_t)queue_id, &attr);
      return status;
    }

    sai_thrift_status_t sai_thrift_clear_queue_stats(const sai_thrift_object_id_t queue_id,
        const std::vector<sai_thrift_queue_stat_counter_t> & thrift_counter_ids,
        const int32_t number_of_counters) {
      printf("sai_thrift_clear_queue_stats\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_queue_api_t *queue_api;
      status = sai_api_query(SAI_API_QUEUE, (void **) &queue_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_queue_stat_t *counter_ids = (sai_queue_stat_t *) malloc(sizeof(sai_queue_stat_t) * thrift_counter_ids.size());
      std::vector<int32_t>::const_iterator it = thrift_counter_ids.begin();
      for (uint32_t i = 0; i < thrift_counter_ids.size(); i++, it++) {
        counter_ids[i] = (sai_queue_stat_t) *it;
      }

      status = queue_api->clear_queue_stats(
          (sai_object_id_t) queue_id,
          number_of_counters,
          (const sai_stat_id_t *)counter_ids);

      free(counter_ids);
      return status;
    }

    sai_thrift_object_id_t sai_thrift_create_buffer_profile(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      printf("sai_thrift_create_buffer_profile\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_buffer_api_t *buffer_api;
      sai_object_id_t buffer_id = 0;
      status = sai_api_query(SAI_API_BUFFER, (void **) &buffer_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_buffer_attributes(thrift_attr_list, attr_list);
      uint32_t attr_count = thrift_attr_list.size();
      buffer_api->create_buffer_profile(&buffer_id, gSwitchId, attr_count, attr_list);

      return buffer_id;
    }

    void sai_thrift_parse_buffer_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_BUFFER_PROFILE_ATTR_POOL_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        case SAI_BUFFER_PROFILE_ATTR_BUFFER_SIZE:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        case SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        case SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
          attr_list[i].value.u8 = attribute.value.u8;
          break;
        case SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        case SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        case SAI_BUFFER_PROFILE_ATTR_XON_TH:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        }
      }
    }

    sai_thrift_object_id_t sai_thrift_create_pool_profile(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      printf("sai_thrift_create_pool\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_buffer_api_t *buffer_api;
      sai_object_id_t pool_id = 0;
      status = sai_api_query(SAI_API_BUFFER, (void **) &buffer_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_pool_attributes(thrift_attr_list, attr_list);
      uint32_t attr_count = thrift_attr_list.size();
      buffer_api->create_buffer_pool(&pool_id, gSwitchId, attr_count, attr_list);
      return pool_id;
    }

    void sai_thrift_parse_pool_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_BUFFER_POOL_ATTR_TYPE:
          attr_list[i].value.u32 = attribute.value.s32;
          break;
        case SAI_BUFFER_POOL_ATTR_SIZE:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        case SAI_BUFFER_POOL_ATTR_THRESHOLD_MODE:
          attr_list[i].value.u32 = attribute.value.s32;
          break;
        }
      }
    }

    void sai_thrift_get_buffer_pool_stats(std::vector<int64_t> &thrift_counters,
        const sai_thrift_object_id_t buffer_pool_id,
        const std::vector<sai_thrift_buffer_pool_stat_counter_t> &thrift_counter_ids) {
      printf("sai_thrift_get_buffer_pool_stats\n");

      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_buffer_api_t *buffer_api;
      status = sai_api_query(SAI_API_BUFFER, (void **) &buffer_api);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to query buffer_api, status: %d", status);
        return;
      }

      thrift_counters.reserve(thrift_counter_ids.size());
      thrift_counters.resize(thrift_counter_ids.size(), 0);
      status = buffer_api->get_buffer_pool_stats((sai_object_id_t)buffer_pool_id,
          (uint32_t)thrift_counter_ids.size(),
          (const sai_stat_id_t *)thrift_counter_ids.data(),
          (uint64_t *)thrift_counters.data());
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get_buffer_pool_stats, status: %d", status);
        thrift_counters.resize(0);
      }
    }

    sai_thrift_status_t sai_thrift_clear_buffer_pool_stats(const sai_thrift_object_id_t buffer_pool_id,
        const std::vector<sai_thrift_buffer_pool_stat_counter_t> &thrift_counter_ids) {
      printf("sai_thrift_clear_buffer_pool_stats\n");

      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_buffer_api_t *buffer_api;
      status = sai_api_query(SAI_API_BUFFER, (void **) &buffer_api);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to query buffer_api, status: %d", status);
        return status;
      }

      status = buffer_api->clear_buffer_pool_stats((sai_object_id_t)buffer_pool_id,
          (uint32_t)thrift_counter_ids.size(),
          (const sai_stat_id_t *)thrift_counter_ids.data());
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to clear_buffer_pool_stats, status: %d", status);
        return status;
      }
      return SAI_STATUS_SUCCESS;
    }

    sai_thrift_status_t sai_thrift_set_priority_group_attribute(const sai_thrift_object_id_t pg_id, const sai_thrift_attribute_t& thrift_attr) {
      printf("sai_thrift_set_priority_group_attribute\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_buffer_api_t *buffer_api;
      status = sai_api_query(SAI_API_BUFFER, (void **) &buffer_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_attribute_t attr;
      attr.id = thrift_attr.id;
      attr.value.oid = thrift_attr.value.oid;
      status = buffer_api->set_ingress_priority_group_attribute((sai_object_id_t)pg_id, &attr);
      return status;
    }

    void sai_thrift_get_pg_stats(std::vector<int64_t> & thrift_counters,
        const sai_thrift_object_id_t pg_id,
        const std::vector<sai_thrift_pg_stat_counter_t> & thrift_counter_ids,
        const int32_t number_of_counters) {
      printf("sai_thrift_get_pg_stats\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_buffer_api_t *buffer_api;
      status = sai_api_query(SAI_API_BUFFER, (void **) &buffer_api);
      if (status != SAI_STATUS_SUCCESS) {
        return;
      }
      sai_ingress_priority_group_stat_t *counter_ids = (sai_ingress_priority_group_stat_t *) malloc(sizeof(sai_ingress_priority_group_stat_t) * thrift_counter_ids.size());
      std::vector<int32_t>::const_iterator it = thrift_counter_ids.begin();
      uint64_t *counters = (uint64_t *) malloc(sizeof(uint64_t) * thrift_counter_ids.size());
      for (uint32_t i = 0; i < thrift_counter_ids.size(); i++, it++) {
        counter_ids[i] = (sai_ingress_priority_group_stat_t) *it;
      }

      status = buffer_api->get_ingress_priority_group_stats((sai_object_id_t) pg_id,
          number_of_counters,
          (const sai_stat_id_t *)counter_ids,
          counters);

      for (uint32_t i = 0; i < thrift_counter_ids.size(); i++) {
        thrift_counters.push_back(counters[i]);
      }
      free(counter_ids);
      free(counters);
      return;
    }

    sai_thrift_object_id_t sai_thrift_create_wred_profile(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      printf("sai_thrift_create_wred_profile\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_wred_api_t *wred_api;
      sai_object_id_t wred_id = 0;
      status = sai_api_query(SAI_API_WRED, (void **) &wred_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_wred_attributes(thrift_attr_list, attr_list);
      uint32_t attr_count = thrift_attr_list.size();
      wred_api->create_wred(&wred_id, gSwitchId, attr_count, attr_list);
      free(attr_list);
      return wred_id;
    }

    void sai_thrift_parse_wred_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list, sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_WRED_ATTR_GREEN_ENABLE:
          attr_list[i].value.booldata = attribute.value.booldata;
          break;
        case SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        case SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        case SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        case SAI_WRED_ATTR_YELLOW_ENABLE:
          attr_list[i].value.booldata = attribute.value.booldata;
          break;
        case SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        case SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        case SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        case SAI_WRED_ATTR_RED_ENABLE:
          attr_list[i].value.booldata = attribute.value.booldata;
          break;
        case SAI_WRED_ATTR_RED_MIN_THRESHOLD:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        case SAI_WRED_ATTR_RED_MAX_THRESHOLD:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        case SAI_WRED_ATTR_RED_DROP_PROBABILITY:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        case SAI_WRED_ATTR_WEIGHT:
          attr_list[i].value.u8 = attribute.value.u8;
          break;
        case SAI_WRED_ATTR_ECN_MARK_MODE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        }
      }
    }

    sai_thrift_status_t sai_thrift_remove_wred_profile(const sai_thrift_object_id_t wred_id) {
      printf("sai_thrift_remove_wred_profile\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_wred_api_t *wred_api;
      status = sai_api_query(SAI_API_WRED, (void **) &wred_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      status = wred_api->remove_wred((sai_object_id_t) wred_id);
      return status;
    }

    void sai_thrift_parse_tunnel_attributes(const std::vector<sai_thrift_attribute_t> & thrift_attr_list,sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_TUNNEL_ATTR_TYPE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        case SAI_TUNNEL_ATTR_UNDERLAY_INTERFACE :
          attr_list[i].value.oid = attribute.value.oid;
          break;
        case SAI_TUNNEL_ATTR_OVERLAY_INTERFACE:
          attr_list[i].value.oid =attribute.value.oid;
          break;
        case SAI_TUNNEL_ATTR_ENCAP_SRC_IP:
          sai_thrift_parse_ip_address(attribute.value.ipaddr, &attr_list[i].value.ipaddr);
          break;
        case SAI_TUNNEL_ATTR_ENCAP_TTL_MODE :
          attr_list[i].value.u32=attribute.value.u32;
          break;
        case SAI_TUNNEL_ATTR_ENCAP_DSCP_MODE :
          attr_list[i].value.u32=attribute.value.u32;
          break;
        case SAI_TUNNEL_ATTR_ENCAP_TTL_VAL :
          attr_list[i].value.u8=attribute.value.u8;
          break;
        case SAI_TUNNEL_ATTR_ENCAP_DSCP_VAL :
          attr_list[i].value.u8 = attribute.value.u16;
          break;
        case SAI_TUNNEL_ATTR_DECAP_TTL_MODE :
          attr_list[i].value.u32=attribute.value.u32;
          break;
        case SAI_TUNNEL_ATTR_DECAP_DSCP_MODE:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        default:
          break;
        }
      }
    }

    void sai_thrift_parse_tunnel_entry_attributes(const std::vector<sai_thrift_attribute_t> & thrift_attr_list ,sai_attribute_t *attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_VR_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;
        case SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TYPE:
          attr_list[i].value.u32 = attribute.value.u32;
          break;
        case SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_DST_IP:
        case SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_SRC_IP:
          sai_thrift_parse_ip_address(attribute.value.ipaddr, &attr_list[i].value.ipaddr);
          break;
        case SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TUNNEL_TYPE:
          attr_list[i].value.s32=attribute.value.s32;
          break;
        case SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_ACTION_TUNNEL_ID:
          attr_list[i].value.oid=attribute.value.oid;
          break;
        default:
          break;
        }
      }
    }

    sai_thrift_object_id_t sai_thrift_create_tunnel(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      printf("sai_thrift_create_tunnel\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_tunnel_api_t *tunnel_api;

      sai_object_id_t tunnel_id = 0;
      status = sai_api_query(SAI_API_TUNNEL, (void **) &tunnel_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_tunnel_attributes(thrift_attr_list,attr_list);
      uint32_t list_count = thrift_attr_list.size();
      status = tunnel_api->create_tunnel(&tunnel_id, gSwitchId, list_count, attr_list);
      free(attr_list);
      return tunnel_id;
    }

    sai_thrift_status_t sai_thrift_remove_tunnel(const sai_thrift_object_id_t thrift_tunnel_id) {
      printf("sai_thrift_remove_tunnel\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_tunnel_api_t *tunnel_api;
      status = sai_api_query(SAI_API_TUNNEL, (void **) &tunnel_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_object_id_t tunnel_id = (sai_object_id_t ) thrift_tunnel_id;
      status = tunnel_api->remove_tunnel(tunnel_id);
      return status;
    }

    sai_thrift_object_id_t sai_thrift_create_tunnel_term_table_entry(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      printf("sai_thrift_create_tunnel_term_table_entry\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_tunnel_api_t *tunnel_api;
      status = sai_api_query(SAI_API_TUNNEL, (void **) &tunnel_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_object_id_t tunnel_entry_id = 0;
      sai_thrift_parse_tunnel_entry_attributes(thrift_attr_list,attr_list);
      uint32_t list_count = thrift_attr_list.size();
      status = tunnel_api->create_tunnel_term_table_entry(&tunnel_entry_id, gSwitchId, list_count, attr_list);
      free(attr_list);
      return tunnel_entry_id;
    }

    sai_thrift_status_t sai_thrift_remove_tunnel_term_table_entry(const sai_thrift_object_id_t thrift_tunnel_entry_id) {
      printf("sai_thrift_remove_tunnel_term_table_entry\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_tunnel_api_t *tunnel_api;
      status = sai_api_query(SAI_API_TUNNEL, (void **) &tunnel_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }
      sai_object_id_t tunnel_entry_id = (sai_object_id_t ) thrift_tunnel_entry_id;
      status = tunnel_api->remove_tunnel_term_table_entry(tunnel_entry_id);
      return status;
    }

    sai_thrift_object_id_t sai_thrift_create_qos_map(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();
      sai_thrift_attribute_t attribute;
      sai_attribute_t *attr_list;
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_qos_map_api_t *qos_map_api;
      sai_object_id_t qos_map_id = 0;
      sai_qos_map_t *qos_map_list = NULL;

      printf("sai_thrift_create_qos_map\n");

      status = sai_api_query(SAI_API_QOS_MAP, (void **) &qos_map_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }

      attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());

      for (uint32_t i = 0; i < thrift_attr_list.size(); i++, it++) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;

        switch (attribute.id) {
        case SAI_QOS_MAP_ATTR_TYPE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;

        case SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
          sai_attribute_t *attr = &attr_list[i];

          attr->value.qosmap.count = attribute.value.qosmap.count;

          qos_map_list = (sai_qos_map_t *) malloc(attr->value.qosmap.count * sizeof(sai_qos_map_t));
          attr->value.qosmap.list = qos_map_list;

          for (int32_t j = 0; j < attribute.value.qosmap.count; j++) {
            sai_thrift_parse_qos_map_params(&attribute.value.qosmap.map_list[j].key, &attr->value.qosmap.list[j].key);
            sai_thrift_parse_qos_map_params(&attribute.value.qosmap.map_list[j].value, &attr->value.qosmap.list[j].value);
          }
          break;
        }
      }

      qos_map_api->create_qos_map(&qos_map_id, gSwitchId, thrift_attr_list.size(), attr_list);

      free(qos_map_list);
      free(attr_list);
      return qos_map_id;
    }

    void sai_thrift_parse_qos_map_params(const sai_thrift_qos_map_params_t *thrift_qos_params, sai_qos_map_params_t *qos_params) {
      qos_params->tc = thrift_qos_params->tc;
      qos_params->dscp = thrift_qos_params->dscp;
      qos_params->dot1p = thrift_qos_params->dot1p;
      qos_params->prio = thrift_qos_params->prio;
      qos_params->pg = thrift_qos_params->pg;
      qos_params->queue_index = thrift_qos_params->queue_index;
      qos_params->color = (sai_packet_color_t) thrift_qos_params->color;
    }

    sai_thrift_status_t sai_thrift_remove_qos_map(const sai_thrift_object_id_t qos_map_id) {
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_qos_map_api_t *qos_map_api;

      printf("sai_thrift_remove_qos_map\n");

      status = sai_api_query(SAI_API_QOS_MAP, (void **) &qos_map_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }

      status = qos_map_api->remove_qos_map((sai_object_id_t) qos_map_id);
      return status;
    }

    void sai_thrift_parse_debug_counter_attributes(const std::vector<sai_thrift_attribute_t> &thrift_attr_list,
        sai_attribute_t *attr_list,
        int32_t **in_debug_counter_ids_list,
        int32_t **out_debug_counter_ids_list) {
      printf("sai_thrift_parse_debug_counter_attributes\n");

      sai_thrift_attribute_t                              attribute;
      std::vector<sai_thrift_attribute_t>::const_iterator it = thrift_attr_list.begin();

      for (uint32_t i = 0; i < thrift_attr_list.size(); ++i, ++it) {
        attribute = (sai_thrift_attribute_t)*it;
        attr_list[i].id = attribute.id;
        switch (attribute.id) {
        case SAI_DEBUG_COUNTER_ATTR_IN_DROP_REASON_LIST:
          {
            *in_debug_counter_ids_list = (int32_t *) malloc(sizeof(int32_t) * attribute.value.s32list.count);
            if (!in_debug_counter_ids_list) {
              return;
            }
            for (uint32_t reason_idx = 0; reason_idx < attribute.value.s32list.s32list.size(); ++reason_idx) {
              (*in_debug_counter_ids_list)[reason_idx] = attribute.value.s32list.s32list[reason_idx];
            }
            attr_list[i].value.s32list.count = attribute.value.s32list.count;
            attr_list[i].value.s32list.list = *in_debug_counter_ids_list;
            break;
          }
        case SAI_DEBUG_COUNTER_ATTR_OUT_DROP_REASON_LIST:
          {
            *out_debug_counter_ids_list = (int32_t *) malloc(sizeof(int32_t) * attribute.value.s32list.count);
            if (!out_debug_counter_ids_list) {
              return;
            }
            for (uint32_t reason_idx = 0; reason_idx < attribute.value.s32list.s32list.size(); ++reason_idx) {
              (*out_debug_counter_ids_list)[reason_idx] = attribute.value.s32list.s32list[reason_idx];
            }
            attr_list[i].value.s32list.count = attribute.value.s32list.count;
            attr_list[i].value.s32list.list = *out_debug_counter_ids_list;
            break;
          }
        case SAI_DEBUG_COUNTER_ATTR_TYPE:
          attr_list[i].value.s32 = attribute.value.s32;
          break;
        default:
          break;
        }
      }
    }

    sai_thrift_object_id_t sai_thrift_create_debug_counter(const std::vector<sai_thrift_attribute_t> & thrift_attr_list) {
      printf("sai_thrift_create_debug_counter\n");

      sai_debug_counter_api_t    *debug_counter_api;
      sai_status_t                status                     = SAI_STATUS_SUCCESS;
      sai_object_id_t             debug_counter_id           = {};
      int32_t                    *in_debug_counter_ids_list  = NULL;
      int32_t                    *out_debug_counter_ids_list = NULL;

      status = sai_api_query(SAI_API_DEBUG_COUNTER, (void **) &debug_counter_api);
      if (status != SAI_STATUS_SUCCESS) {
        return debug_counter_id;
      }

      sai_attribute_t *attr_list = (sai_attribute_t *) malloc(sizeof(sai_attribute_t) * thrift_attr_list.size());
      sai_thrift_parse_debug_counter_attributes(thrift_attr_list,
          attr_list,
          &in_debug_counter_ids_list,
          &out_debug_counter_ids_list);
      uint32_t list_count = thrift_attr_list.size();

      status = debug_counter_api->create_debug_counter(&debug_counter_id,
          gSwitchId,
          list_count,
          attr_list);

      free(attr_list);
      free(in_debug_counter_ids_list);
      free(out_debug_counter_ids_list);

      return debug_counter_id;
    }

    sai_thrift_status_t sai_thrift_remove_debug_counter(const sai_thrift_object_id_t thrift_debug_counter_id) {
      printf("sai_thrift_remove_debug_counter\n");

      sai_debug_counter_api_t *debug_counter_api;
      sai_status_t             status = SAI_STATUS_SUCCESS;

      status = sai_api_query(SAI_API_DEBUG_COUNTER, (void **) &debug_counter_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }

      status = debug_counter_api->remove_debug_counter((sai_object_id_t) thrift_debug_counter_id);

      return status;
    }

    sai_thrift_status_t sai_thrift_set_debug_counter_attribute(const sai_thrift_object_id_t dc_id, const sai_thrift_attribute_t &thrift_attr) {
      printf("sai_thrift_set_debug_counter_attribute\n");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_debug_counter_api_t *debug_counter_api;
      int32_t                 *in_debug_counter_ids_list  = NULL;
      int32_t                 *out_debug_counter_ids_list = NULL;

      status = sai_api_query(SAI_API_DEBUG_COUNTER, (void **) &debug_counter_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }

      std::vector<sai_thrift_attribute_t> thrift_attr_list;
      thrift_attr_list.push_back(thrift_attr);
      sai_attribute_t attr;
      sai_thrift_parse_debug_counter_attributes(thrift_attr_list, &attr, &in_debug_counter_ids_list, &out_debug_counter_ids_list);

      status = debug_counter_api->set_debug_counter_attribute((sai_object_id_t)dc_id, &attr);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to set debug counter attribute.");
      }

      free(in_debug_counter_ids_list);
      free(out_debug_counter_ids_list);

      return status;
    }

    sai_thrift_status_t sai_thrift_get_switch_stats(std::vector<int64_t>              &thrift_counters,
        const sai_thrift_object_id_t             switch_id,
        const std::vector<sai_thrift_stat_id_t> &thrift_counter_ids) {
      printf("sai_thrift_get_switch_stats\n");

      sai_switch_api_t *switch_api;
      sai_status_t      status = SAI_STATUS_SUCCESS;

      status = sai_api_query(SAI_API_SWITCH, (void **) &switch_api);
      if (status != SAI_STATUS_SUCCESS) {
        return status;
      }

      sai_stat_id_t *counter_ids = (sai_stat_id_t *) malloc(sizeof(sai_stat_id_t) * thrift_counter_ids.size());
      if (!counter_ids) {
        return SAI_STATUS_NO_MEMORY;
      }
      std::vector<int32_t>::const_iterator it = thrift_counter_ids.begin();
      for (uint32_t i = 0; i < thrift_counter_ids.size(); i++, it++) {
        counter_ids[i] = (sai_stat_id_t) *it;
      }

      uint64_t *counters = (uint64_t *) malloc(sizeof(uint64_t) * thrift_counter_ids.size());
      if (!counters) {
        free(counter_ids);
        return SAI_STATUS_NO_MEMORY;
      }
      status = switch_api->get_switch_stats((sai_object_id_t) switch_id,
          thrift_counter_ids.size(),
          (const sai_stat_id_t *)counter_ids,
          counters);

      for (uint32_t i = 0; i < thrift_counter_ids.size(); i++) {
        thrift_counters.push_back(counters[i]);
      }

      free(counter_ids);
      free(counters);
      return status;
    }

    int64_t sai_thrift_get_switch_stats_by_oid(const sai_thrift_object_id_t thrift_counter_id) {
      printf("sai_thrift_get_switch_stats_by_oid\n");

      sai_debug_counter_api_t           *debug_counter_api;
      std::vector<sai_thrift_stat_id_t>  thrift_counter_ids;
      std::vector<int64_t>               thrift_counters;
      sai_status_t                       status     = SAI_STATUS_SUCCESS;
      sai_attribute_t                    attr       = {};
      int32_t                            index_base = 0;

      status = sai_api_query(SAI_API_DEBUG_COUNTER, (void **) &debug_counter_api);
      if (SAI_STATUS_SUCCESS != status) {
        return 0;
      }

      attr.id = SAI_DEBUG_COUNTER_ATTR_TYPE;
      status = debug_counter_api->get_debug_counter_attribute((sai_object_id_t) thrift_counter_id, 1, &attr);
      if (SAI_STATUS_SUCCESS != status) {
        return 0;
      }

      switch (attr.value.s32) {
      case SAI_DEBUG_COUNTER_TYPE_SWITCH_IN_DROP_REASONS:
        index_base = SAI_SWITCH_STAT_IN_DROP_REASON_RANGE_BASE;
        break;
      case SAI_DEBUG_COUNTER_TYPE_SWITCH_OUT_DROP_REASONS:
        index_base = SAI_SWITCH_STAT_OUT_DROP_REASON_RANGE_BASE;
        break;
      default:
        printf("Unsupported debug counter type '%d'\n", attr.value.s32);
        return 0;
      }

      attr.id = SAI_DEBUG_COUNTER_ATTR_INDEX;
      status = debug_counter_api->get_debug_counter_attribute((sai_object_id_t) thrift_counter_id, 1, &attr);
      if (SAI_STATUS_SUCCESS != status) {
        return 0;
      }

      thrift_counter_ids.push_back((sai_thrift_stat_id_t)(index_base + attr.value.s32));

      status = sai_thrift_get_switch_stats(thrift_counters, gSwitchId, thrift_counter_ids);
      if (SAI_STATUS_SUCCESS != status) {
        return 0;
      }

      return thrift_counters[0];
    }

    //
    // SAI Next Hop Group API *****************************************************************************************
    //

    void sai_thrift_parse_next_hop_group_attributes
      (sai_attribute_t *attr_list, const std::vector<sai_thrift_attribute_t> &thrift_attr_list) noexcept {
        if (thrift_attr_list.empty() || attr_list == nullptr) { SAI_THRIFT_LOG_ERR("Invalid input arguments."); }

        std::vector<sai_thrift_attribute_t>::const_iterator cit = thrift_attr_list.begin();

        for (sai_uint32_t i = 0; i < thrift_attr_list.size(); i++, cit++) {
          sai_thrift_attribute_t attribute = *cit;
          attr_list[i].id = attribute.id;

          switch (attribute.id) {
          case SAI_NEXT_HOP_GROUP_ATTR_TYPE:
            attr_list[i].value.s32 = attribute.value.s32;
            break;

          default:
            SAI_THRIFT_LOG_ERR("Failed to parse attributes.");
            break;
          }
        }
      }

    sai_thrift_object_id_t sai_thrift_create_next_hop_group(const std::vector<sai_thrift_attribute_t> &thrift_attr_list) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_next_hop_group_api_t *nhop_group_api = nullptr;
      auto status = sai_api_query(SAI_API_NEXT_HOP_GROUP, reinterpret_cast<void**>(&nhop_group_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return SAI_NULL_OBJECT_ID;
      }

      sai_attribute_t *attr_list = nullptr;
      sai_uint32_t attr_size = thrift_attr_list.size();
      sai_thrift_alloc_attr(attr_list, attr_size);
      sai_thrift_parse_next_hop_group_attributes(attr_list, thrift_attr_list);

      sai_object_id_t nhop_group_oid = 0;
      status = nhop_group_api->create_next_hop_group(&nhop_group_oid, gSwitchId, attr_size, attr_list);
      sai_thrift_free_attr(attr_list);

      if (status == SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_DBG("Exited.");
        return nhop_group_oid;
      }

      SAI_THRIFT_LOG_ERR("Failed to create group.");

      return SAI_NULL_OBJECT_ID;
    }

    sai_thrift_status_t sai_thrift_remove_next_hop_group(const sai_thrift_object_id_t nhop_group_oid) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_next_hop_group_api_t *nhop_group_api = nullptr;
      auto status = sai_api_query(SAI_API_NEXT_HOP_GROUP, reinterpret_cast<void**>(&nhop_group_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return status;
      }

      status = nhop_group_api->remove_next_hop_group(nhop_group_oid);

      SAI_THRIFT_LOG_DBG("Exited.");

      return status;
    }

    void sai_thrift_parse_next_hop_group_member_attributes(sai_attribute_t *attr_list, const std::vector<sai_thrift_attribute_t> &thrift_attr_list) noexcept {
      if (thrift_attr_list.empty() || attr_list == nullptr) { SAI_THRIFT_LOG_ERR("Invalid input arguments."); }

      std::vector<sai_thrift_attribute_t>::const_iterator cit = thrift_attr_list.begin();

      for (sai_uint32_t i = 0; i < thrift_attr_list.size(); i++, cit++) {
        sai_thrift_attribute_t attribute = *cit;
        attr_list[i].id = attribute.id;

        switch (attribute.id) {
        case SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_GROUP_ID:
        case SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_ID:
          attr_list[i].value.oid = attribute.value.oid;
          break;

        case SAI_NEXT_HOP_GROUP_MEMBER_ATTR_WEIGHT:
          attr_list[i].value.u32 = attribute.value.u32;
          break;

        default:
          SAI_THRIFT_LOG_ERR("Failed to parse attributes.");
          break;
        }
      }
    }

    sai_thrift_object_id_t sai_thrift_create_next_hop_group_member(const std::vector<sai_thrift_attribute_t> &thrift_attr_list) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_next_hop_group_api_t *nhop_group_api = nullptr;
      auto status = sai_api_query(SAI_API_NEXT_HOP_GROUP, reinterpret_cast<void**>(&nhop_group_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return SAI_NULL_OBJECT_ID;
      }

      sai_attribute_t *attr_list = nullptr;
      sai_uint32_t attr_size = thrift_attr_list.size();
      sai_thrift_alloc_attr(attr_list, attr_size);
      sai_thrift_parse_next_hop_group_member_attributes(attr_list, thrift_attr_list);

      sai_object_id_t nhop_group_member_oid = 0;
      status = nhop_group_api->create_next_hop_group_member(&nhop_group_member_oid, gSwitchId, attr_size, attr_list);
      sai_thrift_free_attr(attr_list);

      if (status == SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_DBG("Exited.");
        return nhop_group_member_oid;
      }

      SAI_THRIFT_LOG_ERR("Failed to create group member.");

      return SAI_NULL_OBJECT_ID;
    }

    sai_thrift_status_t sai_thrift_remove_next_hop_group_member(const sai_thrift_object_id_t nhop_group_member_oid) noexcept {
      SAI_THRIFT_LOG_DBG("Called.");

      sai_next_hop_group_api_t *nhop_group_api = nullptr;
      auto status = sai_api_query(SAI_API_NEXT_HOP_GROUP, reinterpret_cast<void**>(&nhop_group_api));

      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("Failed to get API.");
        return status;
      }

      status = nhop_group_api->remove_next_hop_group_member(nhop_group_member_oid);

      SAI_THRIFT_LOG_DBG("Exited.");

      return status;
    }

    // Returns sai_object_id for a system_port_id
    sai_thrift_object_id_t sai_thrift_get_sys_port_obj_id_by_port_id(const int32_t sys_port_id) {
      SAI_THRIFT_LOG_DBG("Called.");
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_switch_api_t *switch_api;
      sai_system_port_api_t *sys_port_api;
      sai_attribute_t attr, max_sys_port_attribute;
      sai_attribute_t sys_port_list_object_attribute;
      sai_attribute_t sys_port_attr;
      int max_sys_ports = 0;
      sai_object_id_t sys_port_obj_id;

      if (sys_port_id < 0) {
        return SAI_NULL_OBJECT_ID;
      }

      status = sai_api_query(SAI_API_SWITCH, (void **) &switch_api);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("sai_api_query failed!!!");
        return SAI_NULL_OBJECT_ID;
      }
      attr.id = SAI_SWITCH_ATTR_TYPE;
      status = switch_api->get_switch_attribute(gSwitchId, 1, &attr);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("get_switch_attribute failed!!!");
        return SAI_NULL_OBJECT_ID;
      }
      if (attr.value.u32 != SAI_SWITCH_TYPE_VOQ) {
        SAI_THRIFT_LOG_ERR("Switch is not VOQ switch!!!");
        return SAI_NULL_OBJECT_ID;
      }
      status = sai_api_query(SAI_API_SYSTEM_PORT, (void **) &sys_port_api);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("sai_api_query failed!!!");
        return SAI_NULL_OBJECT_ID;
      }

      max_sys_port_attribute.id = SAI_SWITCH_ATTR_NUMBER_OF_SYSTEM_PORTS;
      switch_api->get_switch_attribute(gSwitchId, 1, &max_sys_port_attribute);
      max_sys_ports = max_sys_port_attribute.value.u32;

      sys_port_list_object_attribute.id = SAI_SWITCH_ATTR_SYSTEM_PORT_LIST;
      sys_port_list_object_attribute.value.objlist.list = (sai_object_id_t *) malloc(sizeof(sai_object_id_t) * max_sys_ports);
      sys_port_list_object_attribute.value.objlist.count = max_sys_ports;
      status = switch_api->get_switch_attribute(gSwitchId, 1, &sys_port_list_object_attribute);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("get_switch_attribute failed!!!");
        free(sys_port_list_object_attribute.value.objlist.list);
        return SAI_NULL_OBJECT_ID;
      }

      for (int i=0 ; i<max_sys_ports ; i++) {
        sys_port_attr.id = SAI_SYSTEM_PORT_ATTR_CONFIG_INFO;
        status = sys_port_api->get_system_port_attribute(sys_port_list_object_attribute.value.objlist.list[i], 1, &sys_port_attr);
        if (status != SAI_STATUS_SUCCESS) {
          SAI_THRIFT_LOG_ERR("get_system_port_attribute failed!!! for system_port 0x%lx", sys_port_list_object_attribute.value.objlist.list[i]);
          continue;
        }
        if (sys_port_attr.value.sysportconfig.port_id == (uint32_t)sys_port_id) {
          sys_port_obj_id = sys_port_list_object_attribute.value.objlist.list[i];
          free(sys_port_list_object_attribute.value.objlist.list);
          return sys_port_obj_id;
        }
      }

      SAI_THRIFT_LOG_ERR("Didn't find system port port\n");
      free(sys_port_list_object_attribute.value.objlist.list);
      return SAI_NULL_OBJECT_ID;
    }

    void sai_thrift_get_system_port_attribute(sai_thrift_attribute_list_t& thrift_attr_list, const sai_thrift_object_id_t sys_port_oid) {
      SAI_THRIFT_LOG_DBG("sai_thrift_get_system_port_attribute for 0x%lx", sys_port_oid);
      sai_status_t status = SAI_STATUS_SUCCESS;
      sai_system_port_api_t *sys_port_api;
      sai_attribute_t max_voq_attribute;
      sai_attribute_t voq_list_object_attribute;
      sai_thrift_attribute_t thrift_voq_list_attribute;
      sai_object_list_t *voq_list_object;
      int max_voqs = 0;

      if (sys_port_oid == SAI_NULL_OBJECT_ID) {
        SAI_THRIFT_LOG_ERR("Invalid system port!!!");
        return;
      }
      status = sai_api_query(SAI_API_SYSTEM_PORT, (void **) &sys_port_api);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("sai_api_query failed!!!");
        return;
      }

      max_voq_attribute.id = SAI_SYSTEM_PORT_ATTR_QOS_NUMBER_OF_VOQS;
      status = sys_port_api->get_system_port_attribute(sys_port_oid, 1, &max_voq_attribute);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("sai_api_query failed!!!");
        return;
      }
      max_voqs = max_voq_attribute.value.u32;

      voq_list_object_attribute.id = SAI_SYSTEM_PORT_ATTR_QOS_VOQ_LIST;
      voq_list_object_attribute.value.objlist.list = (sai_object_id_t *) malloc(sizeof(sai_object_id_t) * max_voqs);
      voq_list_object_attribute.value.objlist.count = max_voqs;
      status = sys_port_api->get_system_port_attribute(sys_port_oid, 1, &voq_list_object_attribute);
      if (status != SAI_STATUS_SUCCESS) {
        SAI_THRIFT_LOG_ERR("sai_api_query failed!!!");
        return;
      }

      std::vector<sai_thrift_attribute_t>& attr_list = thrift_attr_list.attr_list;
      thrift_voq_list_attribute.id = SAI_SYSTEM_PORT_ATTR_QOS_VOQ_LIST;
      thrift_voq_list_attribute.value.objlist.count = max_voqs;
      std::vector<sai_thrift_object_id_t>& voq_list = thrift_voq_list_attribute.value.objlist.object_id_list;
      voq_list_object = &voq_list_object_attribute.value.objlist;
      for (int index = 0; index < max_voqs; index++) {
        voq_list.push_back((sai_thrift_object_id_t) voq_list_object->list[index]);
      }
      attr_list.push_back(thrift_voq_list_attribute);
      free(voq_list_object_attribute.value.objlist.list);
      SAI_THRIFT_LOG_DBG("Exited.");
    }
};

static void * switch_sai_thrift_rpc_server_thread(void *arg) {
  int port = *(int *) arg;
  shared_ptr<switch_sai_rpcHandler> handler(new switch_sai_rpcHandler());
  shared_ptr<TProcessor> processor(new switch_sai_rpcProcessor(handler));
  shared_ptr<TServerTransport> serverTransport(new TServerSocket(port));
  shared_ptr<TTransportFactory> transportFactory(new TBufferedTransportFactory());
  shared_ptr<TProtocolFactory> protocolFactory(new TBinaryProtocolFactory());

  TSimpleServer server(processor, serverTransport, transportFactory, protocolFactory);
  server.serve();
  return 0;
}

static pthread_t switch_sai_thrift_rpc_thread;

extern "C" {

  int start_sai_thrift_rpc_server(int port) {
    static int param = port;

    std::cerr << "Starting SAI RPC server on port " << port << std::endl;

    int rc = pthread_create(&switch_sai_thrift_rpc_thread, NULL, switch_sai_thrift_rpc_server_thread, &param);
    std::cerr << "create pthread switch_sai_thrift_rpc_server_thread result " << rc << std::endl;

    rc = pthread_detach(switch_sai_thrift_rpc_thread);
    std::cerr << "detach switch_sai_thrift_rpc_server_thread rc" << rc  << std::endl;

    return rc;
  }
}
