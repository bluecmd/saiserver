#!/usr/bin/env bash
# No lab, network, vendor library, or privileged operations. Artifacts are temporary.
set -euo pipefail
cd "$(dirname "$0")/../.."
: "${SAI_HEADER_DIR:?set SAI_HEADER_DIR to official SAI inc/ or installed include/sai}"
THRIFT=${THRIFT:-thrift}
CXX=${CXX:-g++}
build=$(mktemp -d)
trap 'rm -rf "$build"' EXIT
"$THRIFT" -o "$build" --gen cpp -r src/switch_sai.thrift
# EXTRA_CPPFLAGS / EXTRA_LDFLAGS support non-system Thrift installations.
# SAI checkout uses a sibling experimental/; installed packages often nest it.
"$CXX" -std=c++11 -Wall -Wextra -Werror -pedantic -g ${SANITIZE_FLAGS:-} \
  -I"$SAI_HEADER_DIR" -I"$SAI_HEADER_DIR/experimental" -I"$SAI_HEADER_DIR/../experimental" \
  -I"$build/gen-cpp" -Isrc ${EXTRA_CPPFLAGS:-} \
  tests/server/tui_rpc_test.cpp src/tui_rpc.cpp \
  "$build/gen-cpp/sai_tui_types.cpp" "$build/gen-cpp/SaiTui.cpp" \
  "$build/gen-cpp/switch_sai_types.cpp" "$build/gen-cpp/switch_sai_rpc.cpp" \
  ${EXTRA_LDFLAGS:-} -lthrift -pthread -o "$build/tui_rpc_test"
"$build/tui_rpc_test"
