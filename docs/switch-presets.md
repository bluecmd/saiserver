# Switch configuration presets

The TUI separates **loading a local staged configuration** from **applying a
reviewed sequence of hardware operations**. Neither selecting a preset nor
confirming its load sends mutation RPCs. Staging is in memory, not persistent
across TUI restarts.

## Load, inspect, apply

1. Connect to a server with the required bounded API and explicitly enabled
   interface-address responder. Refresh discovery with **r**.
2. Press **p** to list presets and draft the selected preset command. Currently
   the catalog contains `seastone2-32x100g-1x10g`.
3. Press **Enter** to validate and review loading. **y** replaces local staged
   state; **n/Esc** preserves it. Validation failure also preserves it.
4. Use `:preset show` to inspect staged intent.
5. Press **a**, or enter `:preset apply`, to review the complete ordered
   application plan. **y** separately approves application once; **n/Esc** sends
   nothing and preserves staging.

`:presets` lists the catalog; `:preset load ID` selects a named preset. These are
interactive commands, not additions to the single-operation headless CLI.
Review text is scrollable with PageUp/PageDown. Load and apply confirmations
have distinct labels; the load confirmation never implies apply approval.

**Applying is disruptive: all 33 physical ports are disabled first.** Ingress
ACLs are separately attached and verified before forwarding setup. Reused access
bridge ports are explicitly enabled while the physical ports remain down. Each
mirror binding is verified before a separate physical-port enable; the transport
is enabled before mirror sources. Failure or cancellation can leave ports **down**;
there is no automatic restoration to an unfiltered state.

**Apply is not a transaction.** The client resolves symbolic references only
from successful creates with independent matching getters. Each operation
retains its ordinary preflight, mutation, getter, and post-snapshot checks.
Application stops on the first failure or unverifiable readback. There is no
rollback, automatic cleanup, retry, or silent resume. Inspect the audit and
actual state before any recovery. Reapplying onto already-created preset VLANs
is rejected rather than silently replacing them.

Quitting cancels remaining operations. It does not cancel an already-sent
mutation, undo prior steps, or guarantee that a timed-out create did not happen.
Each RPC has its normal timeout; the multi-step operation can take much longer
than one RPC. The UI remains responsive while the bounded worker runs. On quit
during an apply, the TUI waits (bounded) for the in-flight step and its
readback, restores the terminal, and prints the apply audit to stderr.

After an apply that sent any mutation but did not complete, the staged preset
is cleared: a new apply requires reloading and reviewing the preset again.

Plans have a 512-operation ceiling and an 8 MiB audit budget. Per-step audits
retain mutation/getter evidence and snapshot summaries; only the latest complete
inventory is retained, avoiding hundreds of duplicate inventories. Reaching the
audit limit stops further mutations and explicitly reports omitted details.

## Seastone 2 recipe

The mapping comes from the **stock `Seastone_2` HWSKU** retrieved read-only from
`ixp-lab-sw2`, platform `x86_64-cel_seastone_2-r0`. Exact source paths, hashes and
sanitized evidence are in [the platform evidence](evidence/seastone2/README.md).

| Role | Mapping | Configuration |
| --- | --- | --- |
| Access ports 1–32 | `Ethernet0`, `Ethernet4`, …, `Ethernet124`; `Eth1/1`…`Eth32/1`; four hardware lanes each, collectively 1–128 | 100000 Mbps, untagged VLANs 101–132, one separate VLAN per port |
| Transport port 33 | `Ethernet128`, `Eth33/1`, hardware lane 129 | 10000 Mbps, routed port RIF, `192.0.2.1/30`; no preset VLAN membership, ACL or mirror-source binding |

VLAN **N** has one RIF and two operational responder address records:

- IPv4: `10.N.0.1/24`, e.g. `10.101.0.1/24`.
- IPv6: `2001:db8:<decimal digits of N>::1/64`, e.g. `2001:db8:101::1/64`.
  This is **not** hexadecimal formatting of the decimal VLAN number (`65`).

There are **33 RIFs and 65 local addresses**. Host bits are preserved separately
from connected-route prefixes. A dedicated dual-stack virtual router is created.
Connected routes point to each RIF. All 33 ports explicitly reject tagged ingress
and accept untagged ingress (`drop_tagged=true`, `drop_untagged=false`); setting
PVID alone would not prevent tagged injection into another SVI. Separate VLANs provide L2 broadcast-domain
isolation; no additional inter-VLAN isolation policy is requested.

The preset matches **actual discovered lane sets and speed**, never row order,
synthetic OIDs, or a copied runtime OID. Missing, duplicated, overlapping,
broken-out, extra, or wrongly clocked ports reject loading. This checks topology;
it is not independent cryptographic attestation of the chassis model.

**The active `SONIX` HWSKU on sw2 was not the stock layout:** port 3 was broken
out into four 10G ports, producing 36 logical ports. This configuration is
intentionally rejected. The preset does not change ASIC initialization, create
ports, or automatically reconfigure breakout. Establish the stock mode through
a separately authorized platform maintenance procedure first. The dedicated
10G port had no module inserted during collection; traffic operation was not
tested.

Existing default-VLAN memberships on selected bridge ports are explicitly
listed for removal in the apply review. Access bridge ports are reused or
created; the transport bridge port is removed before creating its routed RIF.
Existing target VLANs, non-default memberships, port RIFs, ingress/egress ACLs,
or egress mirror bindings reject compilation instead of being silently deleted.
Limited inventory cannot establish the absence of every foreign dependency;
server errors still stop application and can leave partial effects.

## ERSPAN

All 32 100G ports mirror **egress only** to one enhanced-remote mirror session.
The 10G transport is never a mirror source.

| Parameter | Value |
| --- | --- |
| Outer source IPv4 | `192.0.2.1` |
| Collector IPv4 | `192.0.2.2` |
| Static collector Ethernet MAC | `02:00:00:00:00:02` |
| Outer source MAC | Observed switch router MAC, also explicitly assigned to the RIFs |
| TTL / TOS | 64 / 0 |
| Profile | SAI `MIRROR_L3_GRE_TUNNEL`, IPv4 enhanced remote, GRE protocol `0x88be`, no outer VLAN |

This fixed L3 GRE profile carries the mirrored Ethernet frame directly; it does
**not** add the separate SAI ERSPAN II (8-byte) or III (12-byte) header. Configure
a compatible collector; do not assume a collector requiring those headers will
accept it. Unsupported profile/getter operations fail rather than falling back
to local SPAN or silently claiming success.

The destination MAC is an **illustrative static value selected by user request**,
not a discovered neighbor. The collector must use that MAC for this built-in
recipe. The plan programs a static transport neighbor, IP next hop and collector
host route. Mirror encapsulation uses explicit MAC/IP fields and the monitor
port; it does not perform automatic ARP or derive header fields from that route.

Mirroring 32×100G into 10G is deliberately oversubscribed: full-rate lossless
collection is impossible. Traffic tests and capacity/resource validation remain
separate from configuration correctness.

## Ingress ACL policy

Each 100G port receives one ingress parallel ACL group containing MAC, IPv4 and
IPv6 tables. Four independent deny entries express these three predicates:

1. Source MAC `02:00:00:00:00:aa`, including non-IP Ethernet traffic.
2. TCP destination port `4444`, with explicit protocol 6 in both IPv4 and IPv6
   tables.
3. IPv6 source `2001:db8:dead::1/128`.

These predicates are **OR**, not a conjunction within one entry. No catch-all
permit is inserted into parallel tables; unmatched traffic continues normally
and matching deny entries are not intentionally overridden by another table's
permit. The transport port has no preset ACL binding. SDK table/field/bind-point
support, resource limits, fragment/extension-header handling and cross-table
hardware action resolution must be verified on the target ASIC.

## Operational addresses and limitations

Raw SAI RIFs do not own IP addresses. The separate, opt-in server
`interface_address` service provides real software ARP and IPv6 Neighbor
Advertisement replies through SAI packet callbacks and transmit operations.
See [the server API](server-api.md) and [`interface_address.h`](../src/interface_address.h)
for startup options, ownership, SDK requirements and lifecycle.

The service is **not** merely displayed address intent, but neither is it a full
NOS routing control plane:

- It validates actual RIF MAC, attachment, untagged membership and PVID, and
  refuses ambiguous or stale attachments. Replies are scoped to the ingress
  physical port, preventing identical IPv6 solicited-node groups on different
  VLANs from leaking replies across VLANs.
- It answers valid ARP requests, ordinary IPv6 NS and incoming DAD solicitations.
- IPv6 activation is explicitly **static/no-DAD**: the operator must guarantee
  address uniqueness. The service does not claim to have performed DAD.
- It does not configure Linux addresses, learn/program arbitrary host neighbors,
  provide ICMP echo, or dynamically resolve silent routing destinations.
  Connected routes alone do not resolve destination neighbors. Provision those
  neighbors separately for arbitrary routed traffic; the collector is static.
- Software receive admission and queue limits do not protect the ASIC/SDK CPU
  path from excessive trap traffic. An appropriate policer, or an explicit
  unpoliced-CPU acknowledgement, is required by the backend.
- The SDK must support callback delivery, COPY traps, enumeration, required
  getters and pipeline-bypass send, with intact Ethernet/tag metadata.
  No SDK support or successful wire forwarding is inferred from the headers.

Address getters report **software-service observations**, not fictitious ASIC
IP-address getters. Loading requires an enabled compatible server. Successful
software/fake-SAI tests are not proof that the deployed SDK delivers packets.
Existing ACL binding getter limitations can also make an accepted hardware write
unverifiable; apply stops and reports that uncertainty rather than declaring the
preset applied.

## Offline verification

```sh
cargo fmt --manifest-path tui/Cargo.toml --check
cargo clippy --manifest-path tui/Cargo.toml --locked --all-targets -- -D warnings
cargo test --manifest-path tui/Cargo.toml --locked
cargo build --manifest-path tui/Cargo.toml --release --locked
python3 tui/tests/preset_terminal_smoke.py tui/target/release/sai-tui
./bazelw test //...
```

The Rust suite validates the complete topology/operation plan, dependency
resolution, both confirmation boundaries, unsupported configurations, partial
failures and cancellation. PTY tests drive actual keystrokes through a
snapshot-only loopback server and assert that loading and cancelled apply send
no mutations. Fake-SAI and pure-packet tests validate backend attributes,
checksums, ARP/ND replies, attachment isolation, bounds and lifecycle failures.

No preset was applied to a live switch during development. The read-only sw2
configuration retrieval establishes the mapping, not forwarding, ASIC offload,
ERSPAN collector compatibility or actual ARP/NDP delivery. Hardware validation
requires separate authorization; PR publication also requires user approval.
