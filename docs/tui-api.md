# TUI Thrift management contract (v1)

This bounded extension coexists with the legacy saiserver RPCs on the same
binary/buffered Thrift endpoint (default TCP 9090). `idl/sai_tui.thrift` defines
a service inherited by `switch_sai_rpc` for C++; the Rust client only needs this
small IDL. All mutations must be followed by actual SAI getter readback. Never
return cached requested attributes as if they were observed hardware state.

## Wire interface

Namespace `cpp sai_tui`, `py sai_tui`; service `SaiTui`:

- `Inventory tui_snapshot()`
- `Object tui_get(string kind, string key)`
- `Object tui_create(string kind, map<string,string> attributes)`
- `Object tui_set(string kind, string key, map<string,string> attributes)`
- `void tui_remove(string kind, string key)`
- `map<string,i64> tui_port_counters(string key)`

Every method declares `throws (1: RpcError error)`.
`RpcError {1:i32 status, 2:string message}`; SAI status preserved, invalid input
rejected before hardware calls, unsupported feature explicitly reported.
`Object {1:string kind, 2:string key, 3:map<string,string> attributes}`.
`Inventory {1:list<Object> objects, 2:list<string> warnings}`.

OID keys and references accept decimal or `0x` hexadecimal; canonical output is
hexadecimal. Neighbor key = `<rif-oid>@<ip>`; route key = `<vr-oid>@<CIDR>`.
IP and CIDR validation must support IPv4 and IPv6 (prefix networks canonicalized).
Boolean values `true`/`false`. Reject unknown fields instead of silently ignoring.

## Bounded kinds/attributes

Read-only additional attributes (e.g. operational status, lane lists, type) are
allowed. Create-only SAI fields cannot be changed via set; explain replacement.

| kind | create / writable attributes |
|---|---|
| port | existing only: `admin`, `pvid`, `ingress_acl`, `egress_acl`; read `lanes`, `speed`, `oper_status` |
| vlan | `vlan_id` (create-only); read `members` |
| bridge_port | `port`, optional `bridge`, `admin` (default true), `learning` (`hardware`/`disable`); read `type` |
| vlan_member | `vlan`, `bridge_port`, `tagging` (`tagged`/`untagged`); tagging writable |
| virtual_router | `ipv4`, `ipv6` (default true) |
| router_interface | `virtual_router`, exactly one `port` or `vlan`, optional `src_mac`, `mtu`, `ipv4`, `ipv6` |
| next_hop | `router_interface`, `ip` (IP next hop; immutable) |
| neighbor | `router_interface`, `ip`, `mac`; MAC writable |
| route | `virtual_router`, `prefix`, `next_hop`, optional `action` (`forward`/`drop`); next_hop/action writable |
| acl_table | `stage` (`ingress`/`egress`), `family` (`ipv4`/`ipv6`); port bind-point, supports src/dst IP and IP protocol matching |
| acl_entry | `table`, `priority` (u32), `action` (`permit`/`deny`), optional `src`, `dst` CIDRs and `protocol` (u8); enable; action/priority/enable writable; field matches if supported |
| acl_group | `stage` (`ingress`/`egress`), port bind-point, parallel group |
| acl_group_member | `group`, `table`, `priority` |

Port ACL binding uses group OID where hardware requires a group, or table OID
where supported. Detached binding = `0x0`.

FDB objects are read-only: `kind=fdb`, key `<vlan-or-bridge-oid>@<mac>`, attributes
`bridge_port`, `mac`, `vlan` (OID), and type if known. A notification-derived
FDB view MUST be labelled as such, not presented as exhaustive ASIC inventory.

## Discovery and telemetry

Snapshot discovers switch ports/default VLAN/default virtual router/default
bridge/bridge ports through SAI getters and reads managed resources back.
If hardware object enumeration is unavailable, explicitly warn that VLAN/L3/ACL
inventory is limited to defaults and objects created through this management
service during the current server process. This is not a persistence system.
Never fabricate missing resources. Object getters permit inspection of known
keys even where enumeration is unavailable.

`switch` may appear as a read-only object with key equal to switch OID and
`default_vlan`, `default_virtual_router`, `default_bridge`, `src_mac` attributes.
Port counters map: `in_octets`, `out_octets`, `in_packets`, `out_packets`,
`in_errors`, `out_errors`, `in_discards`, `out_discards`. Preserve unsigned
64-bit bit patterns through signed Thrift i64 (Rust casts to u64). If only a
subset of stats is supported, return supported keys and report unavailable
keys, never zero-fill failed counters. Read-only counter sampling, no clearing.

## Safety

No authentication is added: use localhost or an SSH tunnel on an isolated lab.
UI must confirm a mutation and present RPC errors and any partial-effect
readback failures. No implicit retry of mutations. No create/update/delete from
polling. Port access/trunk workflows use separate explicit VLAN member and
PVID steps so each state change and partial failure is visible.
