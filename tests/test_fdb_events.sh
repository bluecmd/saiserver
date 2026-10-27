#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
: "${CXX:=g++}"
: "${SAI_HEADER_DIR:=/usr/include/sai}"
: "${THRIFT:=thrift}"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
"$THRIFT" -out "$tmp" --gen cpp -r src/switch_sai.thrift
flags=(-std=c++11 -Wall -Wextra -ffunction-sections -fdata-sections
       -I"$SAI_HEADER_DIR" -I"$SAI_HEADER_DIR/experimental" -I"$tmp" -Isrc)
"$CXX" "${flags[@]}" -Dmain=saiserver_unused_main -c src/saiserver.cpp -o "$tmp/server.o"
"$CXX" "${flags[@]}" tests/test_fdb_events.cpp "$tmp/server.o" -Wl,--gc-sections -pthread -o "$tmp/test-fdb"
"$tmp/test-fdb"
echo 'FDB notification tests passed (batch, deduplication, move, age, scoped/global flush)'
