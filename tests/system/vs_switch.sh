#!/bin/bash
# Runs inside nsrun's namespaces, chrooted into the Debian rootfs: starts the
# Redis instance libsaivs requires, then saiserver on libsaivs, then "$@".
# Usage: vs_switch.sh [--veth NAME]... [--no-server] COMMAND [ARGS...]
# Each --veth creates an up veth pair NAME <-> peer-NAME to back a switch port
# (named in the profile's lane map); the test sends and receives on peer-NAME.
# --no-server runs COMMAND without starting Redis or saiserver.
set -euo pipefail
export LC_ALL=C LANG=C PATH=/usr/sbin:/usr/bin
while [[ ${1:-} == --veth ]]; do
    ip link add "$2" type veth peer name "peer-$2"
    ip link set "$2" up
    ip link set "peer-$2" up
    shift 2
done
if [[ ${1:-} == --no-server ]]; then
    shift
    exec "$@"
fi
# libsaivs unconditionally opens ASIC_DB via SONiC's fixed config path. In this
# rootfs /var/run is a plain directory (no maintainer scripts ran), not /run.
mkdir -p /var/run/redis/sonic-db
cp /systest/database_config.json /var/run/redis/sonic-db/
redis-server --daemonize yes --save '' --appendonly no --dir /tmp \
    --unixsocket /var/run/redis/redis.sock --port 6379 --bind 127.0.0.1 --logfile /tmp/redis.log
for _ in $(seq 100); do [[ -S /var/run/redis/redis.sock ]] && break; sleep 0.1; done
[[ -S /var/run/redis/redis.sock ]] || { cat /tmp/redis.log; exit 1; }

SAI_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/libsaivs.so.0 \
    stdbuf -oL -eL /systest/bin/saiserver --no-shell -p /systest/vs.profile >/tmp/saiserver.log 2>&1 &
server=$!

rc=0
"$@" || rc=$?
if ! kill -0 "$server" 2>/dev/null; then
    echo "saiserver exited during the test" >&2
    rc=1
fi
if (( rc != 0 )); then
    echo "--- saiserver log (profile echo omitted)" >&2
    grep -v ': NULL$' /tmp/saiserver.log | tail -50 >&2
fi
exit "$rc"
