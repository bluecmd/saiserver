# Live lab verification: sai-tui

**Completed functional checks and restoration on 2026-10-27.** This records
actual Rust/Ratatui + Thrift + ASIC testing, not just RPC acceptance. Important
SDK readback limitations remain explicitly reported as errors; they are **not**
claimed successful verification.

## Evidence

- [Machine-readable results and restoration summary](evidence/sw4-results.json).
- [Selected real CLI commands, getter values and errors](evidence/sw4-command-results.jsonl).
  Repetitive snapshots are reduced to counts/warnings; requested values are not
  substituted for getter observations.
- [Twelve actual counter samples](evidence/sw4-counters.jsonl).
- Recorded terminal cells: [confirmation review](evidence/sw4-tui-review.txt),
  [independent readback](evidence/sw4-tui-readback.txt),
  [live counters/graph](evidence/sw4-tui-counters.txt).
  The corresponding PNGs rasterize these recorded cells, including the graph's
  Unicode Braille dots; they are not mock UI renderings.

![Recorded live counter screen](evidence/sw4-tui-counters.png)

Private `.lab/` retains the full command/stdout/stderr audit, raw ANSI recording,
actions, terminal snapshots, SDK logs, resource journal and baseline configuration.
These are ignored because full switch configuration may be sensitive. Published
results include SHA-256 digests of the raw terminal recording and command audit.
Host clocks were not assumed synchronized; rate calculations use monotonic time.

## Authority, topology and baseline

The user explicitly authorized disruptive ASIC initialization on **ixp-lab-sw4**.
Only sw4 was reinitialized; **sw2 was not configured or modified**. Management
connectivity remained available. EOS changes used isolated test resources.

| Resource | Observed identity |
|---|---|
| SAI host | `ixp-lab-sw4.local.sonix.network`, Dell S5232F, SONiC/Debian 13 |
| Verifier | `ixp-lab-eos1.local.sonix.network`, DCS-7050QX-32S-R, EOS 4.28.7.1M |
| SDK | `libsaibcm 15.2.1.0.0.0.26.3`; `sai_query_api_version` = 11801 (1.18.1) |
| Test link A | sw4 lane 9 / Ethernet8 / port `0x100000009` ↔ EOS Ethernet9/1, 10G |
| Test link B | sw4 lane 10 / Ethernet9 / port `0x10000000a` ↔ EOS Ethernet9/2, 10G |
| Existing ring | sw4 Ethernet120 ↔ sw2, 100G; interrupted by authorized sw4 initialization, then restored |

Baseline collection saved SONiC's configuration tar, running CONFIG_DB, hardware
profile and port/LLDP/service state, plus original EOS interface configuration.
EOS Ethernet9/1–3 originally belonged to Port-Channel4. Ethernet9/4/VLAN904 was
not changed. Test VLAN3901, VRFs `SAI-TUI-A` / `SAI-TUI-B`, and Loopback901/902
were confirmed unused before creation. Separate EOS VRFs prevented local EOS
routing from satisfying the forwarding tests without traversing sw4.

## Build and actual startup

The C++ executable was built in a local Debian trixie compiler container using
GCC14, C++ Thrift0.19 and SAI1.18.1 headers, linked against the **exact sw4 SDK**.
No installed switch SDK packages or saved SONiC configuration were replaced.
The Rust client uses Thrift0.25 binary/buffered TCP; interoperability was tested
against this real inherited `switch_sai_rpc` service on port9090.

The isolated runtime used the existing `docker-syncd-brcm:latest` image, host
networking, required device access, a read-only hwsku mount, and private `/lab`
files. Original `swss`/`syncd` were stopped first; they were not run concurrently
with the test SDK. The startup form was:

```sh
# Inside the authorized, isolated runtime; not a command to run over live SONiC:
cd /lab
LD_LIBRARY_PATH=/lab/lib ./saiserver -p sai.profile --no-shell
```

**Container shared memory matters:** the default64MiB `/dev/shm` caused SIGBUS
while the SDK initialized a136MiB HA mapping. Remounting it at512MiB resolved
startup. Reproduce with `docker run --shm-size=512m ...`, not Docker's default.
The BDE device aliases were supplied inside the runtime. The original platform
BCM breakout configuration was retained. `--no-shell` keeps the Thrift server
running without waiting for an interactive SDK shell.

The actual interactive client ran on sw4, not just locally through a mock:

```sh
ssh -tt ixp-lab-sw4.local.sonix.network \
  'sudo -n ip vrf exec default /home/bluecmd/saitui-lab/sai-tui \
   --endpoint 127.0.0.1:9090 --timeout-ms 10000 --interval-ms 500'
```

`tests/lab/capture_tui.py` recorded a160×48 terminal, bounded keyboard actions,
normal exit0, no timeout, and13 terminal snapshots. The session visited L3,
reviewed `set router_interface 0x9000600000001 mtu=1510`, cancelled once, reviewed
again and confirmed with `y`, fetched the real getter showing1510, then displayed
live counters and a graph. MTU was independently read back and restored to1500.
The headless commands below use **the same parser, confirmation gate, Thrift
client and mutation/readback executor** as interactive `:` commands; every
headless mutation explicitly supplied `--yes`.

## Packet verification method

`tests/lab/eos_packet_probe.py` sent uniquely nonced UDP Ethernet markers and
captured actual reception on the other EOS interface/VRF. It records sequence,
MACs, IP version and TTL/hop-limit, ignores outgoing captures, and changes no
interface configuration. It is restricted to the documented interfaces,
disposable VRF namespaces, test IP ranges, VLAN3901 and bounded packet counts.

Ordinary EOS-generated pings were **not** used as positive forwarding proof:
both VRFs use the same operational chassis MAC, so such traffic can have equal
source and destination MACs. Initial isolated pings were0/3; this is not a
claimed post-configuration failure or success. Unique marker source MACs
`02:00:00:00:a0:01` and `02:00:00:00:b0:01` avoid that ambiguity.

Example of the actual access→trunk verifier command, issued through EOS `enable`:

```sh
bash sudo python3 /tmp/saitui-probe.py \
  --tx-ns ns-SAI-TUI-A --tx-if et9_1 \
  --rx-ns ns-SAI-TUI-B --rx-if vlan3901 \
  --src-ip 198.18.200.1 --dst-ip 198.18.200.2 --count 5
```

Reverse L2 probes transmitted VLAN3901-tagged frames on default-namespace
`et9_2`, receiving untagged frames on `ns-SAI-TUI-A/et9_1`. Each probe uses a fresh
nonce; unrelated traffic and the sender's own outgoing frames do not count.

## Observed results

| Area | Actual external/getter evidence |
|---|---|
| Discovery | Real Thrift snapshot discovered37 ports, defaults, bridge ports and members; missing ACL getters were labelled unavailable, not allowed to hide all ports |
| Access↔trunk | VLAN3901: IPv4 and IPv6, both directions, **5/5 each**, TTL/hop-limit64 unchanged |
| FDB | Enabled learning for a unique marker, then actual SAI FDB getter and snapshot returned `0x2600000f3d@02:00:00:00:a0:01` on bridge port `0x1003a00000009`; learning then disabled again |
| Tagging modification | SDK rejected in-place `set` with-15; separately confirmed remove/create replacement: tagged egress to the routed receiver **0/5**, replacement untagged **5/5** |
| Membership removal | Actual getter confirmed absence; reverse traffic **0/5** after removing the access member |
| VLAN lifecycle | Duplicate create rejected with-6. After acknowledged remove, explicit create of3901 succeeded; getter-only deletion uncertainty remained visible rather than fabricated |
| IPv4 L3 | Real VR, port RIFs, neighbors, IP next hops and remote `/24` routes; both directions **5/5**, TTL63 and actual MAC rewrite |
| IPv6 L3 | Corresponding remote `/64` routes; both directions **5/5**, hop-limit63 and actual MAC rewrite |
| Route update | Remote IPv4 and IPv6 route `action=drop`: **0/5**; `action=forward`: **5/5**, with actual getter observations |
| Route removal | Removed remote IPv4/IPv6 routes: getter-confirmed absence and **0/5** for each family |
| IPv4 ingress ACL | Exact source/destination `/32` plus UDP17: deny **0/5**, unbind while deny still exists **5/5**, rebind **0/5**, update permit **5/5** |
| IPv6 ingress ACL | Exact source/destination `/128` plus next-header17: the same **0/5 → 5/5 → 0/5 → 5/5** sequence |
| Telemetry | Four EOS bursts received **200/200 each**;12 real counter samples; positive RX rates in CLI and actual UI graph |
| Interactive safety | Recorded review, cancellation without mutation, explicit confirmation, independent getter, navigation and normal terminal exit |

### Explicit route proof, not just automatic neighbor forwarding

L3 EOS link addresses were `198.18.201.2/30`, `198.18.202.2/30`,
`fd00:201::2/64`, `fd00:202::2/64`. The SAI RIF MAC was `02:00:00:00:04:01`;
next-hop MAC was EOS `74:83:ef:3f:2c:fd`. Received routed frames had the former
as source and the latter as destination, with TTL/hop-limit63.

Testing only a neighbor's own IP is insufficient: SAI can automatically create
host routes that take precedence over explicit LPM routes. The decisive tests
used EOS Loopback901 in A (`198.19.201.42/32`, `fd00:201:1::42/128`) and
Loopback902 in B (`198.19.202.42/32`, `fd00:202:1::42/128`). TUI-managed routes
were `198.19.201.0/24`, `198.19.202.0/24`, `fd00:201:1::/64` and
`fd00:202:1::/64`, through the link next hops. This setup proved explicit route
forwarding, action changes and deletion rather than merely neighbor host routes.

### Counter interpretation

At500ms UI polling, the recorded screen shows **251937.4bit/s** RX and nonzero
history. The independent1000ms JSON sampler peaked at approximately
**129612.2bit/s**; different sampling intervals need not give identical burst
peaks. Units are bits/sec from actual monotonic elapsed time, not bytes/sec or
an assumed polling interval. Counters were never cleared. Cumulative discards
include earlier test activity; this was a functionality check, not a zero-loss
performance benchmark. All four200-packet telemetry bursts were actually
received200/200 at the external endpoint.

## Unsupported verification paths — intentionally not claimed passed

On this SDK, binding writes work but the port ACL getters return
`ATTR_NOT_IMPLEMENTED` (`-196608`). The client therefore displays a **verification
failure** with `unavailable.ingress_acl`, preserving the acknowledged write and
independent getter separately. Traffic effects above prove bind/unbind behavior;
they do not invent a readable binding attribute.

Some removed empty VLAN/RIF/ACL-group identity getters remain readable; removed
next-hop getters can return `INVALID_PARAMETER` (`-5`). The server/client retain
**unverified removal / possible partial effect** errors, rather than accepting
these as absence. PORT bridge-port and ACL group-member deletion instead checks
actual parent lists, which were supported and verified. Generic object count
returned-15, so inventory remains limited/process-local and FDB remains
notification-derived, getter-verified and nonexhaustive. See
[server-api.md](server-api.md) for precise semantics.

Port RIFs and ingress ACLs were live-tested. VLAN RIFs, egress ACLs, other
protocol matches and arbitrary SDK combinations are implemented/tested only to
the documented bounded contract; **live verification is not claimed for them**.
There is no exhaustive SAI support or production persistence claim.

## Cleanup and baseline comparison

All steps below were observed, not merely planned:

1. Removed test routes, next hops, neighbors, RIFs and VR; recorded each actual
   getter outcome. Route/neighbor/VR absence succeeded; the SDK limitations for
   some other identities remained explicitly unverified. No failed mutation was
   blindly retried. L2/ACL tests were then repeated with the integrated server's
   actual getter/parent-list fixes.
2. Detached ACLs, removed entries/tables/group members and acknowledged group
   removals. Removed test VLAN members/bridge ports and acknowledged VLAN
   removals, including the separate duplicate/recreate lifecycle check.
3. Restored EOS Ethernet9/1–2 from their original saved snippets; removed
   Vlan3901, VLAN3901, Loopback901/902, both test VRFs and their routing enables.
   **Ethernet9/1–4 and Port-Channel4 configuration exactly matched baseline**;
   all four links were connected, with9/1–3 back in Po4 and9/4 still VLAN904.
4. Stopped the test SDK before restarting SONiC. Removed both test Docker
   containers; restored `psample` and `linux_knet_cb`; started original `syncd`
   and `swss`. Both were observed **active**. No test9090 listener remained.
5. Canonical running **CONFIG_DB was exactly equal** to baseline; all **38
   interface rows** (37 physical ports plus PortChannel4), including speeds,
   MTUs, admin/oper state and membership, matched baseline. PortChannel4 was up
   with all three selected members; Ethernet120/sw2 ring and management were up.
   Saved `/etc/sonic/config_db.json` SHA-256 stayed:

   ```text
   dd218a822ae70666722c3641b10ebd3ec0a4cd0f2faac23437526af643e537e7
   ```

6. Removed the EOS probe file and test-generated crash cores. Retained private
   logs/baselines and the built client in sw4's home-directory test artifact
   folder; no test daemon or alternate SDK remains active. sw2 was not changed.

**Current lab state is restored SONiC, not an actively running test saiserver.**
A future live run needs another explicitly authorized isolated SDK session; do
not start a second ASIC owner alongside SONiC just to reconnect the TUI.

## Automated verification

The final source passed:

```sh
cargo fmt --manifest-path tui/Cargo.toml -- --check
cargo clippy --manifest-path tui/Cargo.toml --locked --all-targets -- -D warnings
cargo test --manifest-path tui/Cargo.toml --locked       # 29 Rust tests
cargo build --manifest-path tui/Cargo.toml --release --locked
python3 tui/tests/terminal_smoke.py tui/target/release/sai-tui  # 4 PTY tests
python3 tests/lab/test_packet_probe.py                 # 5 offline probe tests
# In the documented compiler/SDK environment:
SAI_HEADER_DIR=/usr/include/sai tests/server/run.sh
./tests/test_fdb_events.sh
make -j2 THRIFT=/usr/bin/thrift
```

A final context-isolated OpenAI review (same family, not cross-family) identified
that the server also needed the client's conservative composite-key `-19`
restriction. That guard was added afterward and covered by injected C++
neighbor/route tests; live invalid-parent deletion is **not** claimed tested.
The valid-parent functional paths above are unchanged by this error-path guard.

The C++ suites cover strict validation, getter-backed CRUD, partial effects,
wire dispatch/errors, unsupported getters, stale identity/member readback,
counter subsets and FDB event batches/moves/aging/flushes. Legacy C++ unused-
parameter warnings remain; Rust Clippy passes with warnings denied. Automated
results supplement, rather than replace, the separate live evidence above.
