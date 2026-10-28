# Bounded SERVER management API

The `SaiTui` service in `idl/sai_tui.thrift` is inherited by the legacy
`switch_sai_rpc` service. Both use the existing binary/buffered Thrift endpoint
(default TCP 9090). The wire contract is [tui-api.md](tui-api.md). Existing
legacy method signatures remain available in default mode; the bounded methods
come from the small inherited IDL. Explicit `--interface-address` mode rejects
**all legacy RPCs**, including legacy getters, before handler dispatch.

**No authentication or authorization is added. Use localhost/an SSH tunnel on
an isolated lab.** This is an explicit management API, not a reconciliation
controller: no polling-triggered mutations, automatic retries, rollback,
port-mode workflows, or counter clearing are performed. The legacy API remains
available in default/off mode and retains its existing behavior; the bounded API never invokes its
parsers or uses its notification-derived state as getter readback.

## Methods and error behavior

- `tui_snapshot()` returns getter-backed `Inventory.objects` plus warnings.
- `tui_get(kind, key)` reads the supplied object/entry directly through SAI;
  registration is not required.
- `tui_create(kind, attributes)` creates exactly one resource, records its key
  for process-local enumeration, then performs actual SAI getter readback.
- `tui_set(kind, key, attributes)` validates **all** requested syntax/field names
  before writing, sets attributes individually, then performs getter readback.
- `tui_remove(kind, key)` removes once and reads the full SAI observation for
  absence, not just an immutable identity field. `ITEM_NOT_FOUND` confirms
  absence; `INVALID_OBJECT_ID` is accepted only for standalone-OID kinds, never
  composite neighbor/route keys where it can indicate an invalid parent. Another
  failure is reported as an unconfirmed acknowledged removal, not silently treated
  as proof of absence. The enumeration hint is discarded only after confirmation.
- `tui_port_counters(key)` samples supported counters without clearing them.

Errors are declared `sai_tui::RpcError {status, message}`. Original non-success
SAI statuses, including API-query and indexed attribute errors, are preserved.
Invalid syntax, unknown fields, missing fields and immutable-field updates use
`SAI_STATUS_INVALID_PARAMETER`; an unavailable bounded feature/API uses
`SAI_STATUS_NOT_SUPPORTED`. Reference object type, existence, device-supported
ranges/capabilities, dependencies and resource availability are checked by SAI;
their error statuses are not replaced with guessed successes.

There is **no requested-attribute readback cache**. Successful create/set replies
contain observations from real getters (including SAI defaults), not echoed
request values. Entry identity fields come from the canonical SAI entry key,
whose SDK observation comes from the attribute getters. Some SDK identity
getters remain readable after deletion: see the explicit limitations below. Failed readback after
a successful mutation raises the original getter status with **`READBACK FAILED`
(mutation not rolled back)** and the resource kind/key. The created key remains
in the enumeration registry even if readback failed. A set failure reports the
failed SAI attribute ID and number of preceding successful writes; partial
effects are possible, even when a failing driver call itself has effects.
After any preceding successful writes, getter readback is still attempted and
observed values are included in the error message; if that also fails, the
message includes `PARTIAL READBACK FAILED` and the getter status. The original
mutation failure remains the RPC status. Inspect with `tui_get` before deciding
what to do; **do not blindly retry**.

Some SDKs cannot read every attribute: SONiC's virtual switch, for example,
returns `NOT_IMPLEMENTED` for attributes left at their SAI defaults. Such a
getter (`NOT_SUPPORTED`, `NOT_IMPLEMENTED` or their indexed attribute forms) on
a **writable** attribute is reported as `unavailable.<name>` with the original
status, plus an inventory warning, instead of hiding the whole object. It is
never treated as verified. Getter failures stay fatal for attributes the
current mutation wrote (`READBACK FAILED`), for create-only attributes that
identify the object (e.g. the mirror session profile, an ACL entry's table),
for any other status, and when no attribute of the object is readable at all.

All bounded calls are serialized against other bounded calls by a process mutex.
With the interface-address responder enabled, SAI access additionally shares its
read/validate/TX mutex. Legacy RPCs and the vendor diagnostic shell are disabled
in that mode, including after responder faults. This is not a transaction or a
lock against an external SDK client/process.

## Operational interface-address responder (explicit opt-in)

Default is **off**. The standalone server (`//:server`) uses `src/sai_dynamic.cpp`;
set `SAI_LIBRARY_PATH` to an absolute SDK DSO filename at deployment, before the
first SAI call. No vendor library is needed to build. Required legacy entrypoints
retain their checked, sticky dispatch. Optional `sai_get_object_key`,
`sai_object_type_query`, `sai_switch_id_query`, and
`sai_query_attribute_enum_values_capability` wrappers resolve lazily from the
**same pinned SDK handle**. Missing optional entrypoints do not prevent disabled
mode startup; enabled startup fails closed rather than inventing capabilities.

Explicit startup example (not a hardware validation recipe):

```text
saiserver --profile sai.profile --interface-address \
  --interface-address-static-ipv6-no-dad \
  --interface-address-allow-unpoliced-cpu
```

Alternatively replace `--interface-address-allow-unpoliced-cpu` with
`--interface-address-policer <nonzero-OID>`. The supplied policer must be an
existing same-switch SAI policer; it is borrowed, attached to the owned trap
group, and never changed or removed. Its configuration/effectiveness remains the
operator's responsibility. No policer is automatically created. Without one,
the explicit acknowledgement means **software-only admission, NO ASIC CPU
policer or SDK/ASIC delivery-rate guarantee**: 100 admitted packets/second,
64 queued packets, 2048 bytes/packet, at most 16 callback attributes and 256
addresses. Queue contention can drop packets.

`--interface-address-static-ipv6-no-dad` acknowledges **STATIC IPv6, NO DAD**:
the operator must guarantee address uniqueness. It is required for CLI enable,
even for an initially IPv4-only inventory. The backend also independently rejects
IPv6 creates without it. Incoming DAD solicitations are answered correctly; this
does not mean the configured address performed DAD. Acknowledgement/policer flags
without `--interface-address` are errors. Enabled mode forces the diagnostic
shell off (no alternate topology mutation path).

Before `create_switch`, the server installs `SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY`
in the create attributes. Before starting RPC admission, the backend reads it
back, checks identity, getters, trap enumeration and CB/COPY/bypass enum
capabilities, refuses conflicting existing ARP/ND traps, and creates only its
own trap group, two COPY traps and per-trap callback tables. A failure aborts
startup; no RPC listener is started and no preset can be applied.

Use the existing bounded methods with kind `interface_address`:

```text
tui_create("interface_address", {
  "router_interface": "0x3e9",
  "ingress_port": "0xc9",
  "address": "192.0.2.1/24"
})
# canonical key: 0x3e9@192.0.2.1/24 (NOT 192.0.2.0/24)
tui_get("interface_address", "0x3e9@192.0.2.1/24")
tui_remove("interface_address", "0x3e9@192.0.2.1/24")
```

The three create fields are exact and create-only. Unknown/missing fields fail;
`tui_set` is unsupported. IPv6 host CIDRs are canonicalized without masking, e.g.
`0x3e9@2001:db8::1234/64`. Create/get/snapshot report actual service inventory and
revalidate SAI attachment/MAC, not fabricated SAI address-object readback.
Additional fields are read-only: `state=configured`,
`observation_source=software-responder`, the verified RIF `mac`,
`dad=static-no-dad` for IPv6 (`not-applicable` for IPv4), and
`neighbor_learning=unsupported`. Remove deletes the actual service registration.
There is no persistent registry and no OS address/interface/route configuration.

Supported attachment is a direct physical routed RIF or a VLAN RIF with exactly
one untagged physical bridge-port member and matching port PVID. LAGs, subports,
trunks, ambiguous ingress mappings and stale attachments fail closed. All bounded
SAI create/set/remove calls are conservatively rejected with `OBJECT_IN_USE`
while any interface address exists: remove addresses first, then change topology,
then recreate addresses. Responder validation and TX share the SAI mutex; each
packet revalidates attachment/MAC before transmission. Interface-address dispatch
and snapshot inventory run **outside** that mutex to avoid self-deadlock.

This sends real software ARP replies and IPv6 Neighbor Advertisements through
SAI hostif pipeline-bypass TX. It does **not** implement dynamic neighbor learning,
ICMP echo, connected routes, FDB programming, or neighbor-object creation. Only
untagged Ethernet is accepted; IPv6 extensions/fragments and oversized packets
are rejected. Runtime SDK errors fault the service and subsequent CRUD/inventory
reports the original error. Stale attachments are suppressed, not remapped.

Switch snapshot advertises `preset_api=1` and
`interface_address_backend=enabled` **only** when the responder is running, IPv6
opt-in is present, and service inventory validation succeeds. Otherwise it reports
`preset_api=0` and `disabled`/`failed`, with warnings and actual last-status/error
where available. These are software capabilities, **never hardware-verified
claims**. Physical SDK CB delivery and preservation of the complete Ethernet
header/**all VLAN tags remain unverified**. An SDK which strips or rewrites tags
is unsupported: software cannot prove ingress scope. Fake tests do not establish
physical CB/COPY/bypass behavior or ASIC policer effectiveness.

SIGINT/SIGTERM are blocked before spawning threads and consumed by the main
thread, not an async handler. SDK shutdown callbacks only request shutdown.
Shutdown closes RPC admission, interrupts listener/client reads and joins the RPC
thread, joins the responder and removes only owned traps/tables/group. Cleanup
failure retains residual IDs/status and a failing process exit; it is not hidden
by later successful SDK teardown. No responder/RPC thread is detached. Callback
unregistration clears only our own callback, under the shared SAI lock; unsupported
unregistration leaves code resident through switch removal/API uninitialization.
The SDK remains pinned. Failed startup rollback is not automatically retried by
shutdown; its residual IDs are logged before SDK teardown. If SDK quiescence fails,
process termination skips static
destruction to keep callback state alive until OS exit. There are no automatic
CRUD retries. The legacy diagnostic shell, when used in default/off mode, must
return from its SDK call before its thread can be joined.

Local verification: `//tests:server_test` and `//tests:interface_address_rpc_test`
cover bounded RPC CRUD/snapshot, memory-buffer legacy rejection and real software
ARP/ND against fake SAI; `//tests:startup_test` covers production CLI/startup
callback ordering and teardown with a fake listener (no socket).
`//tests:interface_address_test` covers the packet/backend seams;
`//tests:sai_dynamic_test` builds fake DSOs to test both optional dispatch and
SDKs missing the new symbols. Physical RPC listener interruption and hardware
receive/TX have not been exercised by these tests.

## Input and representation

- Kinds and attribute names are case-sensitive finite whitelists. Unknown fields
  are errors, never ignored. An empty set request is invalid.
- Object IDs/references are unsigned decimal or `0x` hexadecimal (no signs,
  whitespace, overflow or suffixes). Output uses lowercase canonical `0x` hex.
  Null is accepted only for ACL bindings and a route's `next_hop` (`0x0`).
- Neighbor key: `<rif-oid>@<IPv4-or-IPv6>`.
- Route key: `<vr-oid>@<IPv4-or-IPv6-CIDR>`.
- Interface-address key: `<rif-oid>@<host-IP/prefix>`; **host bits are preserved**.
- FDB key: `<vlan-or-bridge-oid>@<mac>`.
- IPs use strict `inet_pton` parsing. CIDRs require a decimal prefix length
  (`0..32` or `0..128`); route host bits are masked out, but interface-address
  host bits are never masked. IPv6 output is canonicalized
  by `inet_ntop`. Embedded NULs are rejected.
- MACs require six colon-separated, two-hex-digit octets; output is lowercase.
- Booleans are exactly `true`/`false`. Integers are unsigned decimal; priority
  and MTU are u32, protocol is u8. MTU must be nonzero. VLAN ID/PVID is `1..4094`.
- Lists (`lanes`, `members`, `ports`, `egress_mirror_sessions`) are comma-separated values without brackets;
  empty lists are empty strings. OID lists contain canonical hex IDs. SAI list
  reads retry buffer-size negotiation with bounded size (65,536) and retries.
- Additional read-only enum attributes (`type`, `oper_status`) are decimal SAI
  enum values. Unexpected existing enum values are reported numerically rather
  than interpreted as one of the supported writable symbols.

## Resource matrix

All names below are the exact wire keys. Optional create fields omitted by the
caller use SAI defaults unless an explicit default is listed. Fields not in the
set column require replacement (remove/create in dependency order) or are
read-only. All supplied immutable fields on set are rejected, even if unchanged.

| kind | Required create fields | Optional create fields | Supported set fields | Additional readback |
|---|---|---|---|---|
| `port` | existing only; create/remove prohibited | — | `admin`, `pvid`, `ingress_acl`, `egress_acl`, `egress_mirror_sessions`, `speed` | `lanes`, `oper_status` |
| `mirror_session` | `monitor_port`, `src_ip`, `dst_ip`, `src_mac`, `dst_mac`, `ttl`, `tos` | none; fixed profile below | all required create fields | `type`, `encap_type`, `ip_version`, `gre_protocol`, `vlan_header_valid`, `monitor_portlist_valid` |
| `vlan` | `vlan_id` | — | none | `members` (VLAN-member OIDs) |
| `bridge_port` | `port` | `bridge`, `admin` (true), `learning` | `admin`, `learning` | `type`, `bridge` |
| `vlan_member` | `vlan`, `bridge_port`, `tagging` | — | `tagging` | — |
| `virtual_router` | none | `ipv4` (true), `ipv6` (true) | `ipv4`, `ipv6` | — |
| `router_interface` | `virtual_router`, exactly one of `port`/`vlan` | `src_mac`, `mtu`, `ipv4`, `ipv6` | `src_mac`, `mtu`, `ipv4`, `ipv6` | `type`; only applicable `port` or `vlan` |
| `interface_address` | exactly `router_interface`, `ingress_port`, `address` (HOSTCIDR) | none | none; remove/create | `mac`, `state`, `observation_source`, `dad`, `neighbor_learning` (software observations; see below) |
| `next_hop` | `router_interface`, `ip` | — | none | `type` (IP next hops only) |
| `neighbor` | `router_interface`, `ip`, `mac` | — | `mac` | canonical key identity fields |
| `route` | `virtual_router`, `prefix`, `next_hop` | `action` (forward) | `next_hop`, `action` | canonical key identity fields |
| `acl_table` | `stage`, `family` | `src_mac_enabled`, `l4_dst_port_enabled` (defaults below) | none | `src_enabled`, `dst_enabled`, `protocol_enabled`, both optional field enables |
| `acl_entry` | `table`, `priority`, `action` | `src`, `dst`, `protocol`, `src_mac`, `l4_dst_port`, `enable` (true) | `priority`, `action`, `enable`, `src`, `dst`, `protocol`, `src_mac`, `l4_dst_port` | only enabled match fields are returned |
| `acl_group` | `stage` | — | none | `type` (parallel), `members` |
| `acl_group_member` | `group`, `table`, `priority` | — | none | — |

### VLAN/bridge/port

`tagging`: `tagged` / `untagged`. `learning`: `hardware` / `disable`.
Bridge ports created here have SAI type `PORT` and belong to the default 802.1Q
bridge. If `bridge` is supplied it is validated against the getter-backed default
bridge; a different bridge is explicitly unsupported. The conditional
`BRIDGE_ID` attribute is not passed on a PORT create (SAI v1.15 only permits it
for other bridge-port types). For PORT/1Q_ROUTER bridge-port readback, `bridge`
is obtained from the actual switch default-1Q-bridge getter. For other existing
types it is obtained from the bridge-port getter. A 1D_ROUTER port additionally
exposes `router_interface` when available; a 1Q_ROUTER port does **not** expose an
individual VLAN RIF via `RIF_ID`.

VLAN membership and port PVID changes are separate RPCs. The server never
implicitly removes default membership, creates a bridge port, or changes the
port PVID as a side effect of another request.

### L3

Port/VLAN router interfaces, IPv4/IPv6 IP next hops, neighbors and routes use the
corresponding finite SAI attributes and entry APIs. RIF attachment/type, next-hop
IP/RIF, neighbor identity, and route identity are immutable. Route `action` is
`forward` / `drop`; a null next-hop can be supplied for a drop route. A RIF's
inapplicable attachment attributes are not read. Existing unsupported next-hop
types produce an explicit error rather than an incorrectly decoded object.

### IPv4 ERSPAN and port egress mirroring

`mirror_session` uses standalone OID keys and the SAI MIRROR API for create,
set, get and remove, with the same real-readback/error rules as other resources.
All seven create fields are mandatory, including explicit outer `src_mac` and
`dst_mac`; no neighbor resolution, hostif, route, or address configuration is
performed. `monitor_port` is a non-null OID (SAI validates the reference and
supported monitor object type). `src_ip` / `dst_ip` accept only IPv4, MACs use
strict six-octet syntax, and `ttl` / `tos` are decimal u8 (`0..255`). All seven
fields can be updated; all syntax is validated before any SAI query/write.

The bounded profile explicitly creates these fixed SAI attributes:

| Read-only wire field | Getter-backed value | SAI attribute/value |
|---|---|---|
| `type` | `enhanced_remote` | `TYPE = SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE` |
| `encap_type` | `l3_gre` | `ERSPAN_ENCAPSULATION_TYPE = SAI_ERSPAN_ENCAPSULATION_TYPE_MIRROR_L3_GRE_TUNNEL` |
| `ip_version` | `4` | `IPHDR_VERSION = 4` |
| `gre_protocol` | `35006` | `GRE_PROTOCOL_TYPE = 0x88be` |
| `vlan_header_valid` | `false` | `VLAN_HEADER_VALID = false` |
| `monitor_portlist_valid` | `false` | `MONITOR_PORTLIST_VALID = false` |

These fixed fields are **not accepted as create/set inputs**, even with matching
values. They are decoded only after their real getters confirm the profile;
other mirror types, IPv6, tagged outer headers, monitor-port-list sessions and
other GRE/encapsulation profiles return `NOT_SUPPORTED`, not invented compatible
observations. This is the SAI L3 GRE enhanced-remote profile, not support for the
separate SAI ERSPAN II/III encapsulation enums. Getter failures retain the exact
SAI status. Set validates the existing fixed profile before writing. A successful
SAI write followed by a failed getter remains a `READBACK FAILED` error.

`port.egress_mirror_sessions` maps to `SAI_PORT_ATTR_EGRESS_MIRROR_SESSION`.
Set replaces the **entire** list with comma-separated non-null session OIDs;
`""` detaches all sessions. Duplicates (including decimal/hex aliases), empty
items, trailing commas, whitespace, zero, overflow, and more than 65,536 items
are rejected before SAI calls. Device list limits and reference types are left
to SAI. The getter returns the actual list, never the requested list. An
unsupported mirror-list getter is an explicit port observation failure (and a
snapshot warning), not an empty list or successful binding verification.
Unbind explicitly before removing a session; no automatic cleanup is attempted.

`port.speed` maps to the documented create-and-set `SAI_PORT_ATTR_SPEED`, in
**Mbps**, accepting decimal `1..4294967295`. This is a configured-speed setter,
not lane/breakout/autonegotiation control. Hardware-supported speeds and state
constraints are validated by SAI; unsupported speeds preserve its status, with
no guessed speed whitelist, fallback, or retry. Readback uses the configured
speed getter, not the requested speed or operational link speed.

### ACL IPv4/IPv6/MAC, groups and binding

`stage`: `ingress` / `egress`; `family`: `ipv4` / `ipv6` / `mac`.

An IP-family table is created with port bind-point, packet-action support,
source/destination IP fields, and protocol matching. IPv4 maps to `FIELD_SRC_IP`, `FIELD_DST_IP`,
`FIELD_IP_PROTOCOL`; IPv6 maps to `FIELD_SRC_IPV6`, `FIELD_DST_IPV6`,
`FIELD_IPV6_NEXT_HEADER` (the `protocol` wire key). Family is inferred on readback
from actual table-field enable getters (including both protocol families), not
a saved create request. Existing mixed/unspecified tables are labelled
`mixed-or-unspecified`; their entries are outside this bounded interface and
return an explicit unsupported error.

IP-family tables optionally enable `src_mac_enabled=true` and/or
`l4_dst_port_enabled=true`, mapping to `FIELD_SRC_MAC` / `FIELD_L4_DST_PORT`.
Both default to SAI's false, preserving the existing IPv4/IPv6 create attributes
unless explicitly opted in. Both are create-only booleans and are always read
back from SAI, not inferred from entry requests. `family=mac` enables only source
MAC matching, without IP, protocol or EtherType qualifiers, so matches can
include **non-IP Ethernet frames**. It implies `src_mac_enabled=true`; explicitly
setting that false or `l4_dst_port_enabled=true` is invalid. MAC family is inferred
when source MAC is enabled and all bounded IP/protocol/L4 fields are disabled.

Entry `src`/`dst` are CIDRs of the table's family, and `protocol` is an exact u8
match (mask `0xff`). `src_mac` is an exact six-octet MAC (mask
`ff:ff:ff:ff:ff:ff`); no masked-MAC syntax is accepted. `l4_dst_port` is a decimal
u16 (`0..65535`, exact mask `0xffff`) and is bounded to **TCP**: create requires
explicit `protocol=6`; set requires supplied or getter-confirmed existing exact
protocol 6. Changing protocol away from TCP while the port match is enabled is
rejected before writing. Readback of an enabled port match without exact TCP,
or of a non-exact MAC/port mask, returns `NOT_SUPPORTED`, never a misleading
exact match. Each match requires its corresponding table field to be enabled.
Omitted match fields on create are disabled by SAI; disabled
fields are omitted on readback, never fabricated as a `/0` or zero protocol.
Entry `action` is `permit` / `deny` (enabled SAI packet action FORWARD / DROP).
`enable` maps to the entry admin state. Priority/action/admin and match fields
are updateable; field updates first inspect the actual table and reject
unsupported fields or a mismatched family before mutation. This is not a
universal ACL-field editor. Match-field disabling is not represented in v1:
replace the entry to remove a match, or use a `/0` address match if that semantics
is intended. An existing disabled packet action is observed as `disabled`.

Groups use port bind-point and parallel type. Group membership and its priority
are create-only. Port `ingress_acl`/`egress_acl` accepts a group OID (or a table
OID on hardware permitting direct table binding); detach with `0x0`. Unsupported
hardware combinations and capabilities return their SAI status. Binding is a
separate explicit port set; no group creation or port binding happens implicitly.

**Policy composition is explicit.** Match fields within one entry are ANDed.
For “deny source MAC **OR** TCP destination port”, create independent deny entries:
a `family=mac` table with `src_mac`, and separate `ipv4` / `ipv6` tables with
`l4_dst_port_enabled=true` and entries containing `protocol=6,l4_dst_port=<port>`.
Add the tables to a parallel group and bind explicitly. Do not put MAC and TCP
fields into the same entry (that would mean AND), or add catchall permits in
other tables that might defeat denies under device action resolution. No permit,
catchall, entry, group or binding is synthesized by this API. Hardware parallel
table/action resolution must still be verified on the target device.

For an explicit **default-deny allow-A OR allow-B** policy within a suitable
single table, use independent higher-priority permit entries and a lower-priority
matchless deny entry. Do not implement this by competing catchall permit/deny
rules in parallel tables. Priority ordering and cross-table conflicts remain SAI
semantics, not an emulated firewall engine; this offline extension does not claim
hardware forwarding verification.

## Observed SDK limitations and conservative verification

The live Broadcom SAI 1.18.1 results are in [lab-verification.md](lab-verification.md).
These are hardware/version limitations, not simulated or cached successes:

- Port ingress/egress ACL getters return indexed `ATTR_NOT_IMPLEMENTED`
  (`-196608`). Ports remain discoverable, with `unavailable.ingress_acl` /
  `unavailable.egress_acl` containing the original status and corresponding
  inventory warnings. No binding value is fabricated. A successful binding
  write therefore **still fails overall client verification**. External
  deny/unbind/rebind/permit probes independently verify the write's effect.
- PORT bridge-port observations validate the actual default bridge `PORT_LIST`;
  ACL group-member observations validate the actual group `MEMBER_LIST`.
  Those authoritative parent lists resolve SDK identity getters that otherwise
  decode removed members from their OIDs. Parent-list failures are not hidden.
- Full observations avoid falsely treating one stale immutable field as proof
  of presence. Nevertheless, this SDK can still return stale identity/default
  values for removed empty VLANs, RIFs and ACL groups; a removed next hop can
  return `INVALID_PARAMETER` (`-5`) rather than an absence status. Such removal
  results remain **unverified failures / possible partial effects**, not claimed
  successful absence. Arbitrary `-5` or other errors never establish absence.
  Enumeration hints are retained when absence cannot be confirmed, so SDK-stale
  objects/warnings may remain visible. Neither a getter's success nor omission
  from a nonexhaustive snapshot is a general hardware-existence oracle.
- In-place VLAN-member tagging changes return `NOT_SUPPORTED` (`-15`) on this
  SDK. The operator can inspect the unchanged getter, then separately confirm
  removal and creation with the replacement tagging. No automatic fallback or
  retry is performed. This explicit replacement was traffic-tested.
- Generic `sai_get_object_count` returned `NOT_SUPPORTED` (`-15`); no exhaustive
  object inventory is claimed. Do not infer production persistence from the
  process-local key registry.

SAI may automatically create host routes when neighbors are created. On this
ASIC such host entries take precedence over an explicit LPM route to the same
neighbor address. Test explicit routes with a **remote prefix behind the next
hop**, not just traffic addressed to that neighbor. Remote IPv4/IPv6 route
forward/drop/update/removal behavior was independently verified.

## Discovery and read-only resources

Snapshot walks the actual switch port list, default VLAN, default virtual router,
default 1Q bridge, VLAN-member/bridge-port lists, reachable 1D-bridge RIFs, and
mirror sessions referenced by observed port egress mirror lists.
Switch-default discovery is attempted independently even if another switch
attribute (such as `src_mac`) cannot be read. It also reads every key created by
this management service during this process. The registry stores **only keys**,
never attribute values. Failed per-object reads become warnings; no partially
filled object is emitted. Duplicate discovered/managed keys are suppressed.

`switch` is read-only with `default_vlan`, `default_virtual_router`,
`default_bridge`, `src_mac`, plus software capability/status attributes
`preset_api`, `interface_address_backend`, `interface_address_last_status`, and
`interface_address_last_error` (see below). Additional read-only `bridge` objects have `type`
and `ports`. `fdb` is read-only with `bridge_port`, `mac`, `vlan` (bridge/VLAN OID)
and `type`; known-key getters use the SAI FDB API.

Warnings always state that this is **not exhaustive ASIC enumeration** and **not
persistent**: non-default VLAN/L3/ACL/mirror objects from legacy calls, another
client, or a previous process are not discoverable through the process registry.
Unbound external mirror sessions require a known-key getter; bound sessions can
be discovered through port egress lists. Mirror read failures become warnings,
not partial or cached objects.
Default 1Q router bridge ports do not expose individual VLAN RIF IDs. Snapshot
does not fabricate RIFs or infer their OIDs. FDB snapshot keys come from legacy
notifications copied under the FDB mutex; each object's attributes are then read
through the actual SAI FDB getter, outside that mutex. Keys are deduplicated,
aged/missing entries are omitted, other failures become warnings. This remains
notification-derived, nonexhaustive inventory, not an ASIC FDB dump. Known-key
`tui_get` still works without registration.

## Port counter availability

The allowed keys are `in_octets`, `out_octets`, `in_packets`, `out_packets`,
`in_errors`, `out_errors`, `in_discards`, `out_discards`. Octets/errors/discards
map to SAI IF counters. Packets sum unicast + multicast + broadcast in the
corresponding direction using unsigned modular u64 arithmetic. Each individual
counter is read independently. Packet totals require all three components.

**A missing allowed key reports that counter as unavailable.** The map-only wire
result has no warning field: clients must compare against the eight-key set and
display missing keys as unavailable, never as zero. Only explicit unsupported,
not-implemented, or single-stat invalid-attribute statuses cause omission. Other
SAI errors are propagated (not converted to omissions or zeroes), including a
real failure in one packet component when another is unsupported. An entirely
unavailable sample raises `NOT_SUPPORTED`. No successful sample is substituted
for a failed sample. Signed Thrift i64 values preserve the u64 bit pattern;
clients interpret them as unsigned. No counters are cleared and no rates are
fabricated by the server. The individual samples are not an atomic ASIC snapshot.

## Build and offline verification

Bazel builds the generated `SaiTui` service/types (`//idl:switch_sai_cc`), the
adapter (`//:server_lib`) and the server from pinned sources; see
[bazel.md](bazel.md). Generated sources are not committed, and no vendor
`libsai` is needed to build: the server loads it at startup.

```sh
# No vendor library or hardware is used by these tests:
bazel test //tests:tests
# Optionally under a sanitizer from the hermetic toolchain (one at a time):
bazel test --config=asan //tests:tests
bazel test --config=ubsan //tests:tests
```

The stub suite tests strict prevalidation without SAI queries, finite attribute
marshalling, IPv4/IPv6 L3 CRUD and CIDR canonicalization, IPv4/IPv6 ACL CRUD,
groups/members/binding, actual observed-vs-requested readback, preserved errors,
partial writes, failed readback after create/set/remove, default discovery,
counter subset/unsigned behavior and inherited binary-Thrift dispatch/errors.
The suite and syntax checks also pass against the locally cached development
headers from Broadcom `libsaibcm-dev_15.2.1.0.0.0.26.3` (those headers identify
SAI 1.18.1). These are offline API/stub tests, **not** ASIC compatibility or
forwarding tests by themselves. The integrated executable was subsequently
linked against the exact sw4 vendor library and tested on hardware using C++
Thrift 0.19 with the Rust 0.25 client; see the separate live verification record.
Full executable linking requires the vendor library.

The preset backend extension is also covered offline: all IPv4 L3-GRE mirror
attributes, CRUD, known-key and bound-session discovery, egress mirror-list
replacement/detach, speed marshalling, exact MAC/TCP ACL fields and masks,
MAC-only/non-IP table construction, independent deny entries, malformed and
unsupported inputs, original errors, partial writes and failed readback. Local
SAI 1.18.1 headers (`saimirror.h`, `saiport.h`, `saiacl.h`) were inspected; the
pinned Bazel build uses the same release, so `bazel test //tests:tests`
reproduces this coverage.

This extension has **not** been deployed or tested against live ASICs. No
Rust/UI, generated Thrift, hostif/address-control-plane or deployment changes are
required by the map-based backend schema.
