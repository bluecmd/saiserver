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
for test in tui_rpc_test interface_address_rpc_test; do
"$CXX" -std=c++11 -Wall -Wextra -Werror -pedantic -g ${SANITIZE_FLAGS:-} \
  -I"$SAI_HEADER_DIR" -I"$SAI_HEADER_DIR/experimental" -I"$SAI_HEADER_DIR/../experimental" \
  -I"$build/gen-cpp" -Isrc ${EXTRA_CPPFLAGS:-} \
  "tests/server/$test.cpp" src/tui_rpc.cpp src/interface_address.cpp \
  "$build/gen-cpp/sai_tui_types.cpp" "$build/gen-cpp/SaiTui.cpp" \
  "$build/gen-cpp/switch_sai_types.cpp" "$build/gen-cpp/switch_sai_rpc.cpp" \
  ${EXTRA_LDFLAGS:-} -lthrift -pthread -o "$build/$test"
timeout 45 "$build/$test"
done
# Real main + fake SDK/listener: no bind(), SDK DSO, signal injection or hardware.
"$CXX" -std=c++11 -Wall -Wextra -Werror -Wno-unused-parameter -pedantic -g ${SANITIZE_FLAGS:-} \
  -I"$SAI_HEADER_DIR" -I"$SAI_HEADER_DIR/experimental" -I"$SAI_HEADER_DIR/../experimental" \
  -I"$build/gen-cpp" -Isrc ${EXTRA_CPPFLAGS:-} \
  tests/server/startup_test.cpp src/saiserver.cpp src/tui_rpc.cpp src/interface_address.cpp \
  "$build/gen-cpp/sai_tui_types.cpp" ${EXTRA_LDFLAGS:-} -lthrift -pthread -o "$build/startup_test"
tests/server/startup_cases.sh "$build/startup_test"
