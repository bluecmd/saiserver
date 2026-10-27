# sai-tui: bounded SAI management client

`sai-tui` is a standalone Rust/Ratatui terminal client for the committed
[`tui-api.md`](tui-api.md) / [`src/sai_tui.thrift`](../src/sai_tui.thrift)
contract. It calls the real `tui_*` methods inherited by `switch_sai_rpc` on the
same **binary protocol / buffered (not framed), non-multiplexed Thrift TCP**
endpoint. It does not use legacy switch RPCs, a REST shim, or simulated state.
No server/lab deployment is performed by building or testing this crate.

## Build and test

Use Rust **1.89+** (the checked-in dependency lockfile requires it):

```sh
cargo build --manifest-path tui/Cargo.toml --release --locked
./tui/target/release/sai-tui --help

cargo fmt --manifest-path tui/Cargo.toml --check
cargo clippy --manifest-path tui/Cargo.toml --locked --all-targets -- -D warnings
cargo test --manifest-path tui/Cargo.toml --locked
# Optional Unix PTY tests: connection failure, explicit reconnect, responsive
# quit during a stalled RPC, signal exit, alternate-screen and termios restoration.
python3 tui/tests/terminal_smoke.py tui/target/release/sai-tui
```

The library, socket mock server, subprocess CLI, and Ratatui test-backend tests
need no switch or lab. They cover the wire methods and declared errors,
malformed/oversized/truncated responses, absolute deadlines, unsigned counters,
confirmation, validation, getter/snapshot readback, partial effects, actual rate
intervals, wrap/reset/missing/reconnect handling, and bounded history/worker input.
PTY tests additionally need Python 3 and a Unix PTY; they make only loopback TCP
connections.

Generated Rust bindings are checked in at `tui/src/sai_tui.rs` and not modified
by hand. To regenerate from the **unchanged** committed small IDL, from the
repository root with Apache Thrift compiler 0.25.0:

```sh
thrift --gen rs -out tui/src src/sai_tui.thrift
cargo fmt --manifest-path tui/Cargo.toml --check
```

There is no Thrift compiler requirement for a normal Cargo build. Rust uses the
matching `thrift` 0.25 runtime; the generated service includes both the client
and the processor used by socket tests. The inherited service dispatches these
methods by their ordinary names, so no multiplexed service prefix is sent.

## Connect safely

**There is no authentication, authorization, encryption, or TLS in this
protocol.** Prefer loopback on an isolated lab host or an SSH tunnel. Do not
expose port 9090 to an untrusted network:

```sh
ssh -N -L 19090:127.0.0.1:9090 user@lab-host
./tui/target/release/sai-tui --endpoint 127.0.0.1:19090 --timeout-ms 2000
```

The default endpoint is `127.0.0.1:9090`. `--endpoint` accepts a **numeric**
IPv4 `IP:port` or IPv6 `[IP]:port`, e.g. `[::1]:9090`. Hostnames are deliberately
not resolved: blocking DNS cannot undermine the RPC deadline. Resolve the host
outside this program or use a loopback tunnel.

`--timeout-ms` is 100..60000 (default 2000) per RPC, including connect, writes,
and the **total** response read time, not merely inactivity between bytes.
Every call opens a new connection; a broken Thrift stream is never reused.
Read-only refresh/sampling may reconnect. **Mutations are never implicitly
retried**, including after timeouts and lost responses. One mutation workflow
normally has four bounded calls: preflight snapshot, mutation, actual getter,
and post-mutation snapshot. A failed create with an unknown allocated OID
cannot have an individual getter; the output explicitly reports this and still
attempts discovery. Neighbor/route composite keys permit getters even when the
create reply was lost.

The UI uses one background worker with capacity-one request and result
channels, at most one outstanding request, no unbounded request queue, and
50 ms terminal event polling. A slow RPC does not block navigation or quitting.
Initial connection failure stays on screen with **r reconnect** instead of
crashing. Terminal guards and a panic hook restore raw mode, cursor, and the
alternate screen on normal quit, I/O errors, and panics. On Unix, SIGINT,
SIGTERM, and SIGHUP request a responsive, nonzero-status exit through the same
cleanup path. Like other terminal programs, forced `SIGKILL` cannot be cleaned
up (`reset` repairs a damaged shell).
**Quitting does not cancel or roll back an already-sent hardware mutation**;
if quitting while busy, reconnect and inspect actual state before acting again.

Wire reads are capped at 16 MiB per response, strings at 1 MiB, containers at
65,536 elements, and protocol recursion at 32. Oversized discovery is an error,
not silently truncated inventory. Input commands are capped at 8192 bytes.

## Interactive operation

```sh
./tui/target/release/sai-tui --endpoint 127.0.0.1:9090 --interval-ms 1000
```

| Key | Action |
| --- | --- |
| `1` .. `7`, `Tab` / `Shift-Tab`, left/right | Ports, VLANs, L2 FDB, L3, ACL, Counters, Help pages |
| `j` / `k`, down/up | Select a discovered resource; details are from the last snapshot |
| `Enter` / `g` | Fetch selected resource using an actual `tui_get` |
| `r` | Discover/refresh/reconnect using `tui_snapshot`; complete JSON and warnings in details |
| `w` | Show full discovery warnings; short status area can wrap/truncate long warnings |
| `:` | Enter a command; field-specific help appears in the details pane |
| `c` | Draft `create KIND`; adjust the kind and supply required fields |
| `e` | Draft `set KIND KEY` for the selection |
| `d` | Review removal of the selected object (not immediate removal) |
| `?` | Field help for the selection (or all kinds if no selection) |
| `PageUp` / `PageDown` | Scroll details, field help, or the complete mutation review |
| `y` | **Only in the review screen**, approve sending the displayed mutation once |
| `n` / `Esc` in review | Cancel without sending any mutation |
| `Esc` while typing | Discard input |
| `l` | Clear details/audit view; resume live counters on the Counters page |
| `q` / `Ctrl-C` | Quit (`Ctrl-C` also works during input/review) |

Entering a mutation command validates it and displays a review; **Enter does
not mutate hardware**. Read the normalized fields and reference warnings in the
scrollable details pane, then explicitly type `y` or cancel. Polling never
creates/sets/removes anything. A mutation audit is sticky: counter polling
pauses while command/getter/discovery results or help are open, so a partial
failure is not immediately hidden by a successful background poll. `l` resumes.

Discovery warnings are part of the data, not decoration. Snapshot inventory
can be limited to switch defaults and objects created through this service in
the **current server process**, rather than exhaustive ASIC enumeration. It is
not persistence. FDB is read-only and may be notification-derived, not an
exhaustive ASIC dump; this is labelled on the FDB page. Known keys not enumerated
can still be inspected with `get KIND KEY`. Never assume an absent discovered
object does not exist.

## Shared command language

Interactive `:` and headless `--command` use exactly the same parser, schema,
reference preflight, confirmation gate, client, and mutation/readback executor:

```text
create KIND name=value ...
set KIND KEY name=value ...
remove KIND KEY
get KIND KEY
counters PORT_OID
help [KIND]
```

Use shell quoting around the entire `--command` argument. Inside a command,
shell-style quoting is accepted for individual words, but there is no shell
execution, expansion, semicolon command chaining, or implicit multi-step batch.
Duplicate/unknown fields, malformed keys/references, invalid booleans/enums,
out-of-range numbers, malformed MACs and IPv4/IPv6 addresses/CIDRs are rejected
locally. OIDs accept decimal or `0x` hex and are normalized to hex; nonzero OIDs
are required except ACL binding `0x0` (detach). Route keys are `VR_OID@CIDR`,
neighbor keys `RIF_OID@IP`, FDB keys `VLAN_OR_BRIDGE_OID@MAC`. CIDRs are normalized
to their network (e.g. `192.0.2.129/24` becomes `192.0.2.0/24`).

Create-only attributes cannot be changed by `set`; perform removal and creation
as **separate confirmed** operations if replacement is appropriate. `set` needs
at least one writable field. RIF creation requires exactly one of `port`/`vlan`.
Known reference object types and known ACL table IP families are checked against
discovery. An unknown OID produces a reference warning and is sent for server
validation: rejecting every non-enumerated OID would make limited discovery
unusable. The server remains authoritative for existence, ACL stages, platform
limits, dependencies, and capabilities. Capability errors preserve the original
SAI status and message; the client never claims unsupported features succeeded.

### Complete field summary

`help KIND` provides required/optional/create-only/writable labels and detailed
field help in either frontend. `get` can show additional read-only attributes.

| Kind | Create fields | Set fields / restrictions |
| --- | --- | --- |
| `port` | Existing only; no create/remove | `admin` bool, `pvid` 1..4094, `ingress_acl`/`egress_acl` table/group OID or `0x0` |
| `vlan` | Required `vlan_id` 1..4094 | No writable fields; read `members` |
| `bridge_port` | Required `port`; optional `bridge`, `admin` (default true), `learning` hardware/disable | `admin`, `learning` |
| `vlan_member` | Required VLAN **OID** `vlan`, `bridge_port`, `tagging` tagged/untagged | `tagging` |
| `virtual_router` | Optional `ipv4`/`ipv6` bool (default true) | `ipv4`, `ipv6` |
| `router_interface` | Required `virtual_router`, exactly one `port`/`vlan`; optional `src_mac`, `mtu`, `ipv4`, `ipv6` | `src_mac`, `mtu` (68..u32 max; hardware may limit), `ipv4`, `ipv6` |
| `next_hop` | Required `router_interface`, IPv4/IPv6 `ip` | Immutable; replace explicitly |
| `neighbor` | Required `router_interface`, IPv4/IPv6 `ip`, `mac` | `mac` |
| `route` | Required `virtual_router`, IPv4/IPv6 CIDR `prefix`, `next_hop`; optional `action` forward/drop | `next_hop`, `action` |
| `acl_table` | Required `stage` ingress/egress, `family` ipv4/ipv6 | Immutable; port bind-point, IP/protocol matching |
| `acl_entry` | Required `table`, `priority` u32, `action` permit/deny; optional `src`/`dst` CIDRs, `protocol` 0..255, `enable` bool | `priority`, `action`, `enable`, capability-dependent `src`, `dst`, `protocol` |
| `acl_group` | Required `stage` ingress/egress | Immutable; port bind-point parallel group |
| `acl_group_member` | Required `group`, `table`, `priority` u32 | Immutable; replace explicitly |
| `fdb` | Read-only | Inspect bridge-port/MAC/VLAN/type; no write support |
| `switch` | Read-only | Inspect defaults/source MAC; no write support |

### Headless operation and exit status

```sh
SAI=./tui/target/release/sai-tui
$SAI --endpoint 127.0.0.1:19090 --snapshot
$SAI --command 'help router_interface'
$SAI --command 'get port 0x1000000000001'
$SAI --command 'get route 0x3000000000001@2001:db8:1::/64'
$SAI --command 'counters 0x1000000000001' --samples 10 --interval-ms 1000
$SAI --command 'create vlan vlan_id=100' --yes
# Without --yes the following exits nonzero BEFORE opening a socket:
$SAI --command 'set port 0x1000000000001 admin=false'
```

Examples use illustrative OIDs; discover and substitute real keys. Endpoint
flags apply to each invocation (the default is used if omitted). `--snapshot`
and `--command` are mutually exclusive. `--samples` 1..10000 applies only to
`counters`; `--interval-ms` 100..60000 controls read-only counter sampling.

Stdout is JSON (one formatted document for snapshot/commands, JSON Lines for
counter sampling). Errors from validation, RPCs, or verification produce a
**nonzero exit status** with useful error details in stdout; CLI usage errors
from Clap go to stderr with exit 2. A mutation also logs its explicit approval
on stderr. `get` and `counters` require no `--yes`. A counter sampling failure
prints a gap/error record and exits nonzero rather than hiding failure/retrying.

Mutation output separates `mutation`, independent `readback`, `snapshot`,
reference warnings, and `attribute_mismatches`. Requested attributes are
compared to normalized **observed getter** values; missing/unmatched attributes
are a visible verification failure, not a fabricated successful readback.
For removal, only a server getter error with SAI `ITEM_NOT_FOUND` (`-7`) verifies
absence; unrelated errors never do. A post-mutation getter/snapshot failure is
an overall failure even if the mutation was acknowledged. Errors can have
**partial effects**: review both readbacks and refresh before deciding what to
do next. A timed-out OID create can leave an object whose key is not known to
the client; its output says so and includes the snapshot attempt. There is no
rollback, transaction, automatic cleanup, or automatic mutation retry.

## Explicit workflows

Each line below is a separate review/approval and readback. No convenience
workflow silently bundles mutations. Use actual returned/discovered keys in
place of the labels (and add `--command '...' --yes` for headless use).

### Access and trunk VLANs

```text
create vlan vlan_id=100
create bridge_port port=PORT_OID admin=true learning=hardware
create vlan_member vlan=VLAN_OID bridge_port=BRIDGE_PORT_OID tagging=untagged
set port PORT_OID pvid=100
```

Reuse a discovered bridge port instead of duplicating it when one exists.
Untagged membership controls egress; PVID classifies untagged ingress. They are
independent operations and either can fail, so inspect both readbacks.

For a trunk, create a **tagged membership for each VLAN** on that bridge port:

```text
create vlan_member vlan=VLAN_100_OID bridge_port=BRIDGE_PORT_OID tagging=tagged
create vlan_member vlan=VLAN_200_OID bridge_port=BRIDGE_PORT_OID tagging=tagged
```

Only set PVID if an intended native/untagged VLAN exists. Changing tagging uses
`set vlan_member MEMBER_OID tagging=tagged` (or `untagged`); it does not
implicitly change PVID. Delete members before VLANs/bridge ports if required
by SAI dependencies. Do not remove a default/shared resource without understanding
its consumers.

### IPv4 and IPv6 forwarding

```text
create virtual_router ipv4=true ipv6=true
create router_interface virtual_router=VR_OID vlan=VLAN_OID mtu=1500 ipv4=true ipv6=true
create neighbor router_interface=RIF_OID ip=192.0.2.2 mac=02:00:00:00:00:02
create next_hop router_interface=RIF_OID ip=192.0.2.2
create route virtual_router=VR_OID prefix=198.51.100.0/24 next_hop=V4_NH_OID
create neighbor router_interface=RIF_OID ip=2001:db8::2 mac=02:00:00:00:00:02
create next_hop router_interface=RIF_OID ip=2001:db8::2
create route virtual_router=VR_OID prefix=2001:db8:1::/64 next_hop=V6_NH_OID
get neighbor RIF_OID@2001:db8::2
set route VR_OID@2001:db8:1::/64 action=drop
```

A port RIF uses `port=PORT_OID` **instead of** `vlan`. SAI does **not** assign
interface IP addresses and this UI does not add Linux IP aliases. RIF + neighbor
+ next-hop + route expresses ASIC forwarding. Connected/local routes, CPU
termination, ARP/NDP response, host OS addresses, and packet generation are not
implicitly configured. Reverse paths and correct VLAN/port setup are separate
requirements. Remove routes before next hops/neighbors/RIFs/VRs as dependencies
require; every removal still requires confirmation.

### IPv4/IPv6 ACLs and binding

```text
create acl_table stage=ingress family=ipv4
create acl_entry table=V4_TABLE_OID priority=100 action=deny src=192.0.2.0/24 protocol=6 enable=true
create acl_table stage=ingress family=ipv6
create acl_entry table=V6_TABLE_OID priority=100 action=permit src=2001:db8::/32 dst=2001:db8:1::/64 protocol=17 enable=true
create acl_group stage=ingress
create acl_group_member group=GROUP_OID table=V4_TABLE_OID priority=100
create acl_group_member group=GROUP_OID table=V6_TABLE_OID priority=200
set port PORT_OID ingress_acl=GROUP_OID
set acl_entry ENTRY_OID enable=false
set port PORT_OID ingress_acl=0x0
```

Use matching `stage=egress` tables/groups with `egress_acl` for egress. Some
platforms permit direct table binding; others require groups. Tables are
port-bind-point and groups parallel only. Family, stage, bind-point, field
updates, resource limits, and action combinations may be unsupported on a
particular ASIC. These errors are not swallowed or translated into success.
Detach bindings and remove dependent entries/group members before deleting
shared tables/groups, where required.

## Counters and rate history

The Counters page samples the selected port read-only. It displays unsigned
64-bit `in_octets`, `out_octets`, `in_packets`, `out_packets`, `in_errors`,
`out_errors`, `in_discards`, `out_discards`. Thrift signed i64 bit patterns are
cast to u64 (negative wire values are **not** negative counters). Missing keys
are explicitly unavailable, never zero-filled or cleared.

Inbound/outbound graphs use `8 * octet_delta / actual_monotonic_elapsed_seconds`
(**bits/sec**, not bytes/sec and not the requested polling interval). History
is bounded to **120 observations**, with sample-index X axis and autoscaled
bit/s Y axis. Scatter points deliberately omit gaps, so reset/missing data is
not plotted as zero traffic or joined by a misleading line. Headless counter
records include unsigned counters, per-direction rates, actual elapsed seconds,
wall-clock sample timestamp, and notes.

The first successful sample establishes a baseline. Missing fields break that
field's baseline. Ordinary decreases are resets, not giant positive traffic;
a near-u64-maximum to near-zero transition (within u32 range at each end) is
conservatively identified as a wrap and uses wrapping subtraction. Other
ambiguous decreases are treated as resets. Zero/stale (>4 sampling intervals)
intervals and disconnects/errors invalidate the baseline. The next successful
sample after reconnect has no rate. Selection changes clear history so different
ports never share a graph. Management commands also break the baseline. A
restart that happens entirely between successful samples and increases counters
cannot be distinguished from traffic using this wire contract (no boot ID or
counter epoch); long gaps/decreases are detected, but do not infer more.

## Deliberate limits

Only the bounded contract kinds/attributes above are managed. There is no FDB
CRUD, port creation/deletion, speed/lane/breakout configuration, Linux IP
configuration, switch-wide configuration, counter clearing, ACL counters,
non-IP next-hop types, arbitrary ACL fields/actions/bind-points, NAT, LAGs,
transactions, persistence, deployment, or lab traffic tooling. Additional
read-only attributes from the server are shown without inventing support for
writing them. Server inventory and capability warnings are preserved. Real
hardware behavior must be verified on the parent-managed lab; passing local
wire/mock tests is not a hardware validation claim.
