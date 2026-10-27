#!/usr/bin/env bash
# Pure packets + fake SAI only. No SDK library, hardware, sockets, root or Thrift.
set -euo pipefail
cd "$(dirname "$0")/../.."
: "${SAI_HEADER_DIR:?set SAI_HEADER_DIR to official SAI 1.18.1 inc/}"
build=$(mktemp -d)
trap 'rm -rf "$build"' EXIT
"${CXX:-g++}" -std=c++11 -Wall -Wextra -Werror -pedantic -g ${SANITIZE_FLAGS:-} \
  -I"$SAI_HEADER_DIR" -I"$SAI_HEADER_DIR/experimental" -I"$SAI_HEADER_DIR/../experimental" \
  -Isrc tests/server/interface_address_test.cpp src/interface_address.cpp \
  -pthread -o "$build/interface_address_test"
"$build/interface_address_test"
