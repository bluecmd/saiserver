#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
: "${CXX:=g++}"
: "${SAI_HEADER_DIR:=/usr/include/sai}"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
flags=(-std=c++11 -Wall -Wextra
       -I"$SAI_HEADER_DIR" -I"$SAI_HEADER_DIR/experimental" -I"$SAI_HEADER_DIR/../experimental" -Isrc ${EXTRA_CPPFLAGS:-})
"$CXX" "${flags[@]}" tests/test_fdb_events.cpp src/notifications.cpp -pthread -o "$tmp/test-fdb"
"$tmp/test-fdb"
echo 'FDB notification tests passed (batch, deduplication, move, age, scoped/global flush)'
