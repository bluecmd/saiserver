// Operational software ARP/ND responder; no OS interfaces, addresses or routes.
#pragma once
extern "C" {
#include <sai.h>
}
#include <array>
#include <cstddef>
#include <cstdint>
#include <map>
#include <mutex>
#include <stdexcept>
#include <string>
#include <vector>

namespace interface_address {
using Attributes = std::map<std::string, std::string>;
struct Error : std::runtime_error {
    sai_status_t status;
    Error(sai_status_t code, const std::string& message) : std::runtime_error(message), status(code) {}
};
struct Options {
    bool enabled = false;
    // With no hardware policer, explicit acknowledgement is required. Software
    // admission is 100 packets/second, queue 64, packet 2048 bytes, attrs 16.
    // This bounds our work, NOT the SDK/ASIC CPU delivery rate.
    bool allow_unpoliced_cpu = false;
    sai_object_id_t policer = SAI_NULL_OBJECT_ID; // Borrowed, never modified/removed.
    // Static IPv6 addresses require operator-guaranteed uniqueness. No DAD is
    // performed by this backend; opting in is required before IPv6 create.
    bool static_ipv6_no_dad = false;
};
struct Sdk {
    // Pass actual vendor entrypoints (or checked forwarding wrappers). Required
    // even on SDKs that do not export object enumeration: fail closed, no guessing.
    decltype(&sai_api_query) query = nullptr;
    decltype(&sai_get_object_key) keys = nullptr;
    decltype(&sai_object_type_query) object_type = nullptr;
    decltype(&sai_switch_id_query) switch_id = nullptr;
    decltype(&sai_query_attribute_enum_values_capability) enum_values = nullptr;
};
struct Observation {
    std::string key; // canonical hexadecimal RIF OID@hostCIDR (host bits intact)
    Attributes attributes;
};
struct Status {
    bool running = false;
    size_t addresses = 0, queued = 0;
    uint64_t admitted = 0, dropped = 0, sent = 0, rejected = 0, errors = 0;
    sai_status_t last_status = SAI_STATUS_SUCCESS;
    std::string last_error;
    // Owned IDs persist until their remove succeeds; stop() can be retried.
    sai_object_id_t trap_group = 0;
    std::array<sai_object_id_t, 2> traps{{0, 0}}, tables{{0, 0}};
};

sai_packet_event_notification_fn packet_callback() noexcept;
// Single switch per process. Install packet_callback() as
// SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY BEFORE create_switch (preferred). start()
// reads it back and refuses to run if absent/different/unsupported. Setter use is
// only safe if the SDK supports it and getter verifies the value. Do not replace
// another consumer's callback. No hooks are silently installed by this module.
//
// sai_mutex MUST serialize ALL other SAI topology mutations with our read+send,
// and outlive stop(). Never call these APIs with sai_mutex already held. Dispatch
// interface_address RPCs BEFORE acquiring tui_rpc's normal SAI mutex, and pass
// that same mutex here. This prevents a topology change between validation/TX.
void start(sai_object_id_t switch_id, const Options&, const Sdk&, std::mutex& sai_mutex);
// Stops admission, joins worker, then removes only owned tables/traps/group in
// dependency order. Throws on cleanup failure, retains IDs for retry. After stop
// returns/throws the worker is joined and callbacks are harmless no-ops. Before
// process/library teardown unregister the switch callback under sai_mutex and
// quiesce SDK callbacks (remove_switch/uninitialize according to SDK contract).
// Do NOT unload this module while SDK callbacks can still execute.
void stop();
Observation create(sai_object_id_t switch_id, const Attributes&);
Observation get(sai_object_id_t switch_id, const std::string& key);
void remove(sai_object_id_t switch_id, const std::string& key);
std::vector<Observation> list(sai_object_id_t switch_id);
Status status();

// Pure packet seam, also used by worker. Untagged Ethernet only; no IPv6
// extensions/fragments, jumbo payloads, neighbor learning or arbitrary routing.
// SDK callbacks must preserve the complete Ethernet header and VLAN tags; an SDK
// that strips or rewrites ingress tagging is unsupported (cannot prove scope).
// No ICMP echo responder, connected route, FDB or SAI neighbor is created.
struct Target {
    bool ipv6 = false;
    std::array<uint8_t, 16> ip{};
    std::array<uint8_t, 6> mac{};
};
std::vector<uint8_t> make_reply(const Target&, const uint8_t* packet, size_t size);

/* Integration (parent-owned files):
 * - Compile this .cpp with -std=c++11 -pthread and the official SAI headers.
 * - Explicit CLI opt-in only; default Options leaves service off. Supply Sdk
 *   entrypoints from the same loaded SDK. The standalone sai_dynamic.cpp currently
 *   lacks wrappers for keys/object_type/switch_id/enum_values: extend its checked dispatch or
 *   pass resolved pointers; never substitute fake enumeration. Disabled mode
 *   does not need these symbols. On enabled start failure abort preset apply.
 * - Before switch init append PACKET_EVENT_NOTIFY with value.ptr =
 *   reinterpret_cast<sai_pointer_t>(packet_callback()). After init call start.
 * - tui_rpc kind "interface_address": exactly three create attrs:
 *   router_interface OID, address HOST_IP/PREFIX, ingress_port OID. create/get/
 *   remove/list delegate here OUTSIDE the shared SAI lock; translate Error.status
 *   and what() to RpcError. Object.kind="interface_address", Object.key=obs.key,
 *   Object.attributes=obs.attributes. set is unsupported; remove+create instead.
 *   schema: the three attrs are create-only, remaining observation attrs read-only.
 *   Include list() in snapshot; it is software service inventory, not a hardware
 *   interface-address getter. Never reuse the route-prefix parser (masks hostbits).
 * - Stop RPC traffic, call stop BEFORE switch removal/API uninitialize. Report and
 *   retry cleanup errors using status() residual IDs; never pretend removal worked.
 *   Then under sai_mutex, get PACKET_EVENT_NOTIFY and, only if it is still ours,
 *   set its value.ptr to nullptr and check the status. If setting is unsupported,
 *   keep this code resident through remove_switch/uninitialize and SDK callback
 *   quiescence. Never clear a replacement callback belonging to another consumer.
 * - Runtime SDK receive-validation/TX errors fault the service; subsequent CRUD/
 *   inventory propagates the error. Consult status() and stop/restart only after
 *   fixing the underlying SDK/topology. Stale attachments are suppressed per packet
 *   and rejected by get/list, never silently remapped to a different interface.
 * - VLAN RIFs require exactly one untagged physical bridge-port member and matching
 *   PVID. Routed RIFs require direct physical-port attachment. No LAG/subports,
 *   trunk reception, ambiguous ingress mappings or stale identities are supported.
 *   No fixed 32-port limit: up to 256 addresses accommodate VLANs 101..132 + 10G.
 * - IPv6 is STATIC-NO-DAD, not tentative/duplicate-detected: operator must verify
 *   uniqueness before enabling; the service still answers incoming DAD correctly.
 *   Actual SDK CB/COPY/bypass/getter/enumeration support must be validated in a
 *   separately authorized hardware test. Pure/fake tests are not hardware evidence.
 */
} // namespace interface_address
