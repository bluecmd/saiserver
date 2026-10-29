#!/bin/bash
# Runs the examples/ programs (with only bash and coreutils in the rootfs) against saiserver on libsaivs: both must print
# the same `show interfaces brief` table, listing every switch port and the
# default VLAN 1 with all of them as untagged members.
set -euo pipefail
for _ in $(seq 100); do /systest/bin/show_interfaces_cpp >/tmp/cpp.txt 2>/tmp/cpp.err && break; sleep 0.2; done
/systest/bin/show_interfaces_rust >/tmp/rust.txt
cat /tmp/cpp.txt
if [[ $(</tmp/cpp.txt) != $(</tmp/rust.txt) ]]; then
    echo "C++ and Rust examples disagree; Rust printed:" >&2
    cat /tmp/rust.txt >&2
    exit 1
fi
# libsaivs's BCM56850 model: 32 ports of four lanes at 40G, admin and oper
# down, untagged in VLAN 1.
ports=$(grep -Ec '^0x[0-9a-f]+ +[0-9]+,[0-9]+,[0-9]+,[0-9]+ +40G +down +down +1$' /tmp/cpp.txt)
(( ports == 32 )) || { echo "expected 32 port rows, got $ports" >&2; exit 1; }
read -ra vlan1 <<<"$(grep -E '^1 +untagged ' /tmp/cpp.txt || true)"
(( ${#vlan1[@]} == 34 )) || { echo "expected VLAN 1 to list 32 untagged ports: ${vlan1[*]}" >&2; exit 1; }
echo "PASS: C++ and Rust examples list 32 ports and VLAN 1"
