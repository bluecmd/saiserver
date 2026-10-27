# Live lab verification record

Status: **in progress — not a completion claim**.

## Authority and topology

The user explicitly granted full authority over **ixp-lab-sw4** for this
project, including disruptive ASIC/server setup. sw2 is not being modified.
EOS changes are limited to isolated test resources and will be restored.
SSH uses the existing `*.local.sonix.network` proxy configuration.

Read-only discovery confirmed:

- sw4: Dell S5232F, SONiC Debian 13, kernel 6.12.41+deb13-sonic-amd64.
- Original SONiC `swss` and `syncd` active and enabled; no saiserver listener.
- Broadcom package `libsaibcm 15.2.1.0.0.0.26.3` reports **SAI 1.18.1** via
  `sai_query_api_version`. Its exact library is used for linking and runtime.
- sw4 physical lanes 9/10 (SONiC Ethernet8/9) connect to EOS Ethernet9/1–2
  at 10 Gb/s. The existing BCM profile already specifies these breakouts.
- EOS: Arista DCS-7050QX-32S-R, EOS 4.28.7.1M.
- Original EOS Ethernet9/1–3 belong to Port-Channel4; Ethernet9/4 is the
  VM attachment on VLAN 904. Tests only detach/reconfigure Ethernet9/1–2.
- sw4 Ethernet120 is the live 100G ring to sw2. ASIC reinitialization on sw4
  necessarily interrupts sw4 forwarding; this is authorized. No sw2 settings
  are modified.

## Baselines and build environment

Private local `.lab/baseline/` holds a tar of sw4's saved config, FRR files,
hardware profile and machine identification, its running CONFIG_DB dump,
port/LLDP/service/route output, checksums, and the original EOS interface
configuration. These are deliberately ignored by Git: they may contain
sensitive configuration. Restore commands for the isolated EOS resources are
prepared in `.lab/eos-restore.cli`.

The sw4 runtime is an isolated `saitui-runtime` container based on the existing
`docker-syncd-brcm:latest` image, with the original platform profile mounted
read-only and a private copy of the BCM config in `/lab`. No SDK replacement
or saved SONiC configuration edits are needed. `saitui-build` was an initial
unused build-container attempt. Package downloads from sw4 are unavailable;
the successful compiler environment is a local Debian trixie Podman container
(`saitui-compiler`) with GCC 14, Thrift 0.19 C++ and official SAI 1.18.1 headers.
It links against the exact sw4 library. Runtime Thrift dependencies are copied
into the private test directory, not installed over switch packages.

## Test isolation

EOS VLAN **3901** and VRFs **SAI-TUI-A** / **SAI-TUI-B** did not exist before
the test. Ethernet9/1 is a routed interface in A, Ethernet9/2 is a trunk allowing
only VLAN 3901, and Vlan3901 is in B. Test addresses initially are
`198.18.200.1/30`, `198.18.200.2/30`, `fd00:3901::1/64`, `fd00:3901::2/64`.
These separate VRFs prevent local EOS routing from satisfying tests without
traversing sw4. The fourth port and VLAN 904 are not reconfigured.

Before any TUI-controlled forwarding, the isolated IPv4 ping produced:

```
ping vrf SAI-TUI-A 198.18.200.2 repeat 3 timeout 1
3 packets transmitted, 0 received, 100% packet loss
```

## Required result matrix

| Check | Evidence/result |
|---|---|
| Interactive Rust/Ratatui session running on sw4 | Pending |
| Thrift snapshot and mutation readback | Pending |
| Access-to-trunk and reverse VLAN forwarding via EOS | Pending |
| Learned FDB inspection | Pending |
| IPv4/IPv6 L3 RIF, neighbor, next-hop, route forwarding | Pending |
| IPv4 ACL deny/permit external traffic comparison | Pending |
| IPv6 ACL deny/permit external traffic comparison | Pending |
| Live counters and nonzero rate graphs during traffic | Pending |
| CRUD cleanup and post-removal readback | Pending |
| EOS baseline restored | Pending |
| SONiC restored and management/links verified | Pending |

Do not mark this record complete based only on successful RPC acceptance.
External traffic checks, actual state getters, and restoration are required.
