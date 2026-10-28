#!/bin/bash
# Runs inside nsrun's namespaces, chrooted into the Debian rootfs: starts the
# Redis instance libsaivs requires, then saiserver on libsaivs, then "$@".
set -euo pipefail
export LC_ALL=C LANG=C PATH=/usr/sbin:/usr/bin
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
