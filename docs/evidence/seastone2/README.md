# Seastone2 read-only platform reconnaissance

Collected from `ixp-lab-sw2.local.sonix.network` on 2026-10-27. Remote collection timestamp: `2026-10-27T15:12:02.913797+00:00` (host clock; SSH wrapper timestamps differed).

## Conclusion

**The installed Seastone2 platform definition supports 32 dedicated 100G QSFP ports plus a separate 33rd 10G SFP port.** The latter is **Ethernet128 / Eth33/1 / front-panel index 33 / hardware lane 129**, not an additional four-lane QSFP or a CPU-only host interface. Platform transceiver code identifies ports 1–32 as QSFP and port 33 as `SFP1`; the running FPGA sysfs exposes `SFP1`. The Broadcom port map configures it as `portmap_66=129:10:m`; the `m` suffix is preserved as evidence, not interpreted here. Running KNET reports Ethernet128 with SDK port 66 and physical port 129, and ASIC_DB contains its SAI NETDEV hostif and 10000 Mbps port speed.

**Physical support is established by platform definitions and runtime enumeration, not a traffic test.** `SFP1/sfp_modabs` was `1` (module absent per platform code), and its SAI hostif operational state was false. No optic insertion, link test, or hardware configuration was performed.

## Identity and active configuration caveat

- ONIE platform: `x86_64-cel_seastone_2-r0`; machine `cel_seastone_2`, revision `0`, architecture `x86_64`.
- Installed default SKU file says `Seastone_2 t1`.
- **Actual `/etc/sonic/config_db.json` HWSKU is `SONIX`**, not `Seastone_2`.
- Stock `Seastone_2/port_config.ini`, `hwsku.json`, and `platform.json` describe the requested 32x100G + 1x10G layout.
- Active `SONIX/port_config.ini` and saved config PORT table break out front-panel port 3 into four 10G interfaces: Ethernet8/9/10/11 on lanes 9/10/11/12, aliases Eth3/1–Eth3/4. Remaining 31 QSFP ports remain 100G; Ethernet128 remains the dedicated 10G port. There are 36 logical ports in this active layout.
- Do not blindly use the active SONIX breakout map as the baseline 32x100G preset.

## Authoritative baseline lane/front-panel map

Speeds are Mbps. For front-panel port `p` in 1..32, SONiC name is `Ethernet(4*(p-1))`, alias is `Ethp/1`, lanes are `[4*p-3, 4*p-2, 4*p-1, 4*p]`, speed 100000. **Lanes are one-based hardware identifiers, not zero-based SONiC interface suffixes or SDK logical port numbers.**

| Front panel | SONiC name | Alias | Hardware lanes | Speed |
|---:|---|---|---|---:|
| 1 | Ethernet0 | Eth1/1 | 1,2,3,4 | 100000 |
| 2 | Ethernet4 | Eth2/1 | 5,6,7,8 | 100000 |
| 3 | Ethernet8 | Eth3/1 | 9,10,11,12 | 100000 |
| 4 | Ethernet12 | Eth4/1 | 13,14,15,16 | 100000 |
| 5 | Ethernet16 | Eth5/1 | 17,18,19,20 | 100000 |
| 6 | Ethernet20 | Eth6/1 | 21,22,23,24 | 100000 |
| 7 | Ethernet24 | Eth7/1 | 25,26,27,28 | 100000 |
| 8 | Ethernet28 | Eth8/1 | 29,30,31,32 | 100000 |
| 9 | Ethernet32 | Eth9/1 | 33,34,35,36 | 100000 |
| 10 | Ethernet36 | Eth10/1 | 37,38,39,40 | 100000 |
| 11 | Ethernet40 | Eth11/1 | 41,42,43,44 | 100000 |
| 12 | Ethernet44 | Eth12/1 | 45,46,47,48 | 100000 |
| 13 | Ethernet48 | Eth13/1 | 49,50,51,52 | 100000 |
| 14 | Ethernet52 | Eth14/1 | 53,54,55,56 | 100000 |
| 15 | Ethernet56 | Eth15/1 | 57,58,59,60 | 100000 |
| 16 | Ethernet60 | Eth16/1 | 61,62,63,64 | 100000 |
| 17 | Ethernet64 | Eth17/1 | 65,66,67,68 | 100000 |
| 18 | Ethernet68 | Eth18/1 | 69,70,71,72 | 100000 |
| 19 | Ethernet72 | Eth19/1 | 73,74,75,76 | 100000 |
| 20 | Ethernet76 | Eth20/1 | 77,78,79,80 | 100000 |
| 21 | Ethernet80 | Eth21/1 | 81,82,83,84 | 100000 |
| 22 | Ethernet84 | Eth22/1 | 85,86,87,88 | 100000 |
| 23 | Ethernet88 | Eth23/1 | 89,90,91,92 | 100000 |
| 24 | Ethernet92 | Eth24/1 | 93,94,95,96 | 100000 |
| 25 | Ethernet96 | Eth25/1 | 97,98,99,100 | 100000 |
| 26 | Ethernet100 | Eth26/1 | 101,102,103,104 | 100000 |
| 27 | Ethernet104 | Eth27/1 | 105,106,107,108 | 100000 |
| 28 | Ethernet108 | Eth28/1 | 109,110,111,112 | 100000 |
| 29 | Ethernet112 | Eth29/1 | 113,114,115,116 | 100000 |
| 30 | Ethernet116 | Eth30/1 | 117,118,119,120 | 100000 |
| 31 | Ethernet120 | Eth31/1 | 121,122,123,124 | 100000 |
| 32 | Ethernet124 | Eth32/1 | 125,126,127,128 | 100000 |
| 33 (SFP1) | Ethernet128 | Eth33/1 | 129 | 10000 |

Stock port_config valid speeds: QSFP `100000,40000`; dedicated SFP `10000,1000`. Stock hwsku defaults: QSFP `1x100G`, FEC `rs`, autoneg `off`; SFP `1x10G`, FEC `none`, autoneg `off`. These are platform defaults, not a recommendation to alter the running switch.

## Host/control plane and hostif mechanism

- Debian 13.7, Linux `6.12.41+deb13-sonic-amd64`, SONiC build `kamel_202611-master-kamel.0-dirty-20261020.191003`, ASIC type `broadcom`.
- Docker, swss, syncd systemd units were active. Container list includes `docker-syncd-brcm`, `docker-orchagent`, `docker-database`, `docker-fpm-frr`, platform monitor, teamd, LLDP, GNMI, management framework, and others captured in JSON.
- Loaded modules include `linux_bcm_knet`, `linux_knet_cb`, `linux_kernel_bde`, and `linux_ngbde`.
- `/proc/bcm/knet/ndev` enumerates the Ethernet interfaces as Broadcom kernel network devices, including Ethernet128 with `port=66`, `phys_port=129`.
- `ASIC_DB` key `ASIC_STATE:SAI_OBJECT_TYPE_HOSTIF:oid:0xd00000000067e` has `SAI_HOSTIF_ATTR_TYPE=SAI_HOSTIF_TYPE_NETDEV`, `SAI_HOSTIF_ATTR_NAME=Ethernet128`, `SAI_HOSTIF_ATTR_OBJ_ID=oid:0x1000000000014`, and `SAI_HOSTIF_ATTR_OPER_STATUS=false`.
- The referenced port object's `SAI_PORT_ATTR_SPEED` is `10000`. `SAI_PORT_ATTR_HW_LANE_LIST` was absent from that ASIC_DB hash; lane evidence instead comes from platform PORT mappings and KNET physical-port enumeration. ASIC_DB is software state, not an independent hardware readback.
- This establishes the existing **SAI NETDEV / Broadcom KNET** hostif path. It does not establish packet trap policy, CPU queue setup, or any saiserver deployment/ownership scheme. No deployment was inspected or changed.

## Sources, hashes, and sanitization

`ixp-lab-sw2-sanitized.json` is the evidence manifest. Every file entry is keyed by its **exact absolute remote path**, with `source_sha256` over original source bytes and either safe full platform mapping content or an explicitly selected extract. Hashes refer to source bytes, not reserialized extracts. Proc/sysfs hashes are point-in-time values. Command-derived evidence records exact argv, return code, stdout, and stderr.

Primary sources (prefix `/usr/share/sonic/device/x86_64-cel_seastone_2-r0/`):

| Relative path | SHA-256 |
|---|---|
| `Seastone_2/port_config.ini` | `2bf2f5c9868646d7209a9aaa6281c4d30a8caa1cdb9eb45a7e801581679f5aa9` |
| `Seastone_2/hwsku.json` | `5bbfcc6fa048fb88f25813af5a6099e2f13cf9fcc8f2103c1bd2b7a05d5f739d` |
| `platform.json` | `8e19cc0f2ec564eddeca21666530c31a339793665de4d434f74afc9561ecce75` |
| `SONIX/port_config.ini` | `529b658bb7578ee6f4873b427c9bfb5ca349a8c9c84e35eb7fb922bbbf225814` |
| `plugins/sfputil.py` | `61ad135af74e65a513df4ac7d6c90567ac717ee472375d15e0e5e6823bfd138c` |

Saved `/etc/sonic/config_db.json` source hash: `c23d7fa16a19768a1ae4a72249570c990be80c1ea9161a74aeb0b4cc80542e42`. Only allowlisted platform metadata and PORT fields were exported. No credential sections, full config, descriptions/topology, MAC addresses, or kernel pointer values are stored in the evidence. BCM files are reduced to `portmap_*` lines; SAI profile to two safe settings. The collector reads JSON locally on the remote host solely to select authorized metadata/PORT fields; unrelated sections are neither displayed nor copied.

## Read-only collection commands

The exact final remote collector is `collect-readonly.py`; it was streamed to Python stdin without creating a remote file:

```sh
ssh -o BatchMode=yes -o ConnectTimeout=8 -o ConnectionAttempts=1 \
  ixp-lab-sw2.local.sonix.network 'python3 -' \
  < docs/evidence/seastone2/collect-readonly.py \
  > docs/evidence/seastone2/ixp-lab-sw2-sanitized.json
```

Initial discovery used `hostname`, `uname -srm`, bounded `find`/`ls` under `/etc/sonic`, the specific platform directory, `/sys/class/net`, and `/proc/bcm`; selected machine/build metadata via `grep`; Python read-only platform-file reads; `systemctl is-active docker swss syncd`; `docker ps --format '{{.Names}} {{.Image}}'`; `sonic-db-cli ASIC_DB KEYS 'ASIC_STATE:SAI_OBJECT_TYPE_HOSTIF:*'`; and targeted `HGETALL`/`HGET` operations shown in the collector. `ethtool -i Ethernet128` produced no stdout with stderr suppressed, so it is not used as evidence. One initial discovery command returned 1 because optional metadata paths were absent. The final collector completed successfully, and all captured subprocesses returned 0.

No sudo, service restart, remote file write, configuration command, SDK shell, or packet injection was used. The platform Python plugin was read as text, never instantiated or executed. No repository code was modified, no tests were rerun for this evidence-only task, and no commit/push/PR was made.

## Remaining limits

No access blocker for the requested platform mapping. The 33rd port lacks an inserted module at observation time, so operational traffic at 10G/1G is unverified. The active host uses a custom breakout SKU, and applying any baseline preset would require separate authorized maintenance and validation. A stock platform.json listing only 1x100G does not negate the separately observed custom SONIX 4x10G breakout; broader breakout capabilities were not probed.
