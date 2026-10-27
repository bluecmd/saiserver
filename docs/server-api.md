# Bounded SERVER management API

The `SaiTui` service in `src/sai_tui.thrift` is inherited by the legacy
`switch_sai_rpc` service. Both use the existing binary/buffered Thrift endpoint
(default TCP 9090). The wire contract is [tui-api.md](tui-api.md). No original
IDLs or Rust code are changed by this server implementation.

**No authentication or authorization is added. Use localhost/an SSH tunnel on
an isolated lab.** This is an explicit management API, not a reconciliation
controller: no polling-triggered mutations, automatic retries, rollback,
port-mode workflows, or counter clearing are performed. The legacy API remains
available and retains its existing behavior; the bounded API never invokes its
parsers or uses its notification-derived state as getter readback.

## Methods and error behavior

- `tui_snapshot()` returns getter-backed `Inventory.objects` plus warnings.
- `tui_get(kind, key)` reads the supplied object/entry directly through SAI;
  registration is not required.
- `tui_create(kind, attributes)` creates exactly one resource, records its key
  for process-local enumeration, then performs actual SAI getter readback.
- `tui_set(kind, key, attributes)` validates **all** requested syntax/field names
  before writing, sets attributes individually, then performs getter readback.
- `tui_remove(kind, key)` removes once and probes a SAI attribute getter for
  absence. `ITEM_NOT_FOUND` or `INVALID_OBJECT_ID` confirms absence. A different
  failure is reported as an unconfirmed successful removal, not silently treated
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
whose existence is established by the attribute getters. Failed readback after
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

All bounded calls are serialized against other bounded calls by a process mutex.
This is not a cross-client hardware transaction or a lock for the legacy API.

## Input and representation

- Kinds and attribute names are case-sensitive finite whitelists. Unknown fields
  are errors, never ignored. An empty set request is invalid.
- Object IDs/references are unsigned decimal or `0x` hexadecimal (no signs,
  whitespace, overflow or suffixes). Output uses lowercase canonical `0x` hex.
  Null is accepted only for ACL bindings and a route's `next_hop` (`0x0`).
- Neighbor key: `<rif-oid>@<IPv4-or-IPv6>`.
- Route key: `<vr-oid>@<IPv4-or-IPv6-CIDR>`.
- FDB key: `<vlan-or-bridge-oid>@<mac>`.
- IPs use strict `inet_pton` parsing. CIDRs require a decimal prefix length
  (`0..32` or `0..128`); host bits are masked out. IPv6 output is canonicalized
  by `inet_ntop`. Embedded NULs are rejected.
- MACs require six colon-separated, two-hex-digit octets; output is lowercase.
- Booleans are exactly `true`/`false`. Integers are unsigned decimal; priority
  and MTU are u32, protocol is u8. MTU must be nonzero. VLAN ID/PVID is `1..4094`.
- Lists (`lanes`, `members`, `ports`) are comma-separated values without brackets;
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
| `port` | existing only; create/remove prohibited | — | `admin`, `pvid`, `ingress_acl`, `egress_acl` | `lanes`, `speed`, `oper_status` |
| `vlan` | `vlan_id` | — | none | `members` (VLAN-member OIDs) |
| `bridge_port` | `port` | `bridge`, `admin` (true), `learning` | `admin`, `learning` | `type`, `bridge` |
| `vlan_member` | `vlan`, `bridge_port`, `tagging` | — | `tagging` | — |
| `virtual_router` | none | `ipv4` (true), `ipv6` (true) | `ipv4`, `ipv6` | — |
| `router_interface` | `virtual_router`, exactly one of `port`/`vlan` | `src_mac`, `mtu`, `ipv4`, `ipv6` | `src_mac`, `mtu`, `ipv4`, `ipv6` | `type`; only applicable `port` or `vlan` |
| `next_hop` | `router_interface`, `ip` | — | none | `type` (IP next hops only) |
| `neighbor` | `router_interface`, `ip`, `mac` | — | `mac` | canonical key identity fields |
| `route` | `virtual_router`, `prefix`, `next_hop` | `action` (forward) | `next_hop`, `action` | canonical key identity fields |
| `acl_table` | `stage`, `family` | — | none | `src_enabled`, `dst_enabled`, `protocol_enabled` |
| `acl_entry` | `table`, `priority`, `action` | `src`, `dst`, `protocol`, `enable` (true) | `priority`, `action`, `enable`, `src`, `dst`, `protocol` | only enabled match fields are returned |
| `acl_group` | `stage` | — | none | `type` (parallel) |
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

### ACL IPv4/IPv6, groups and binding

`stage`: `ingress` / `egress`; `family`: `ipv4` / `ipv6`.

A table is created with port bind-point, packet-action support, source/destination
IP fields, and protocol matching. IPv4 maps to `FIELD_SRC_IP`, `FIELD_DST_IP`,
`FIELD_IP_PROTOCOL`; IPv6 maps to `FIELD_SRC_IPV6`, `FIELD_DST_IPV6`,
`FIELD_IPV6_NEXT_HEADER` (the `protocol` wire key). Family is inferred on readback
from actual table-field enable getters, not a saved create request. Existing
mixed/unspecified tables are labelled `mixed-or-unspecified`; their entries are
outside this bounded single-family interface and return an explicit unsupported
error.

Entry `src`/`dst` are CIDRs of the table's family, and `protocol` is an exact u8
match (mask `0xff`). Omitted match fields on create are disabled by SAI; disabled
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

## Discovery and read-only resources

Snapshot walks the actual switch port list, default VLAN, default virtual router,
default 1Q bridge, VLAN-member/bridge-port lists and reachable 1D-bridge RIFs.
Switch-default discovery is attempted independently even if another switch
attribute (such as `src_mac`) cannot be read. It also reads every key created by
this management service during this process. The registry stores **only keys**,
never attribute values. Failed per-object reads become warnings; no partially
filled object is emitted. Duplicate discovered/managed keys are suppressed.

`switch` is read-only with `default_vlan`, `default_virtual_router`,
`default_bridge`, `src_mac`. Additional read-only `bridge` objects have `type`
and `ports`. `fdb` is read-only with `bridge_port`, `mac`, `vlan` (bridge/VLAN OID)
and `type`; known-key getters use the SAI FDB API.

Warnings always state that this is **not exhaustive ASIC enumeration** and **not
persistent**: non-default VLAN/L3/ACL objects from legacy calls, another client,
or a previous process are not discoverable through the process registry.
Default 1Q router bridge ports do not expose individual VLAN RIF IDs. Snapshot
does not fabricate RIFs or infer their OIDs. FDB enumeration is unavailable;
legacy FDB notifications are deliberately not presented as exhaustive hardware
inventory. Known-key `tui_get` still works without registration.

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

Requires GNU make >= 4.3, a C++11 compiler, Thrift compiler/runtime (tested with
0.25.0), SAI headers and, for the executable, vendor `libsai`. Grouped recursive
codegen targets depend on **both** IDLs; generated `SaiTui` service/type objects
and the adapter are included in `librpcserver.a`. Header dependency files prevent
stale forwarding/IDL builds. Generated sources are not committed.

```sh
# Installed SDK/runtime layout:
make -j4 SAI_HEADER_DIR=/path/include/sai SAI_LIBRARY_DIR=/path/lib

# Official SAI v1.15.0 checkout, archive/object compile without libsai:
make -j4 src/obj/librpcserver.a src/obj/saiserver.o \
  SAI_HEADER_DIR=/path/SAI/inc CPPFLAGS=-I/path/SAI/experimental

# No vendor library or hardware is used by these tests:
SAI_HEADER_DIR=/path/SAI/inc THRIFT=/path/to/thrift tests/server/run.sh
# Non-system Thrift: additionally supply EXTRA_CPPFLAGS and EXTRA_LDFLAGS.
# Optional, when sanitizer runtimes exist:
SAI_HEADER_DIR=/path/SAI/inc SANITIZE_FLAGS='-fsanitize=address,undefined -fno-omit-frame-pointer' \
  tests/server/run.sh
```

The stub suite tests strict prevalidation without SAI queries, finite attribute
marshalling, IPv4/IPv6 L3 CRUD and CIDR canonicalization, IPv4/IPv6 ACL CRUD,
groups/members/binding, actual observed-vs-requested readback, preserved errors,
partial writes, failed readback after create/set/remove, default discovery,
counter subset/unsigned behavior and inherited binary-Thrift dispatch/errors.
The suite and syntax checks also pass against the locally cached development
headers from Broadcom `libsaibcm-dev_15.2.1.0.0.0.26.3` (those headers identify
SAI 1.18.1). These are offline API/stub tests, **not** ASIC compatibility or
forwarding tests. No lab connection, deployment, or mutation was performed. Full executable linking
requires the vendor library and is left to the integration environment.
