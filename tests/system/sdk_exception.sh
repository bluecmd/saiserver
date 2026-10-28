#!/bin/bash
# Without the Redis instance it requires, libsaivs (built with GCC/libstdc++)
# throws a C++ exception out of sai_api_initialize. The loader must contain it
# and fail closed; it used to crash in the unwinder (see bazel/unwinder.bzl).
# The server blocks SIGTERM until it is serving, hence timeout's KILL.
set -euo pipefail
rc=0
SAI_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/libsaivs.so.0 \
    timeout -k 5 30 /systest/bin/saiserver --no-shell -p /systest/vs.profile >/tmp/saiserver.log 2>&1 || rc=$?
if ! grep -q 'SAI loader: exception in sai_api_initialize' /tmp/saiserver.log ||
   ! grep -q 'FATAL: failed to sai_api_initialize: -1' /tmp/saiserver.log || (( rc != 1 )); then
    echo "expected the loader to contain the SDK's exception and exit 1, got exit $rc:" >&2
    grep -v ': NULL$' /tmp/saiserver.log >&2
    exit 1
fi
echo "PASS: SDK exception contained (exit $rc)"
