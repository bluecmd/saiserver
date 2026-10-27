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
opts=(--interface-address --interface-address-static-ipv6-no-dad --interface-address-allow-unpoliced-cpu)
FAKE_STARTUP_MODE=disabled timeout 10 "$build/startup_test" --no-shell
FAKE_STARTUP_MODE=enabled timeout 10 "$build/startup_test" "${opts[@]}"
FAKE_STARTUP_MODE=unregister-unsupported timeout 10 "$build/startup_test" "${opts[@]}"
FAKE_STARTUP_MODE=enabled timeout 10 "$build/startup_test" --interface-address --interface-address-static-ipv6-no-dad --interface-address-policer 8000
expect_failure() {
  local rc=0
  "$@" || rc=$?
  if [[ $rc != 1 ]]; then echo "Expected exit 1, got $rc: $*" >&2; exit 1; fi
}
for mode in bad-callback cleanup-fail rollback-fail remove-fail uninit-fail; do
  expect_failure env FAKE_STARTUP_MODE="$mode" timeout 10 "$build/startup_test" "${opts[@]}"
done
expect_failure "$build/startup_test" --interface-address
expect_failure "$build/startup_test" --interface-address --interface-address-static-ipv6-no-dad
expect_failure "$build/startup_test" --interface-address --interface-address-allow-unpoliced-cpu
expect_failure "$build/startup_test" --interface-address-policer 8000
expect_failure "$build/startup_test" --interface-address --interface-address-static-ipv6-no-dad --interface-address-policer -1
expect_failure "$build/startup_test" --interface-address --interface-address-static-ipv6-no-dad --interface-address-policer 18446744073709551616
echo 'PASS real CLI/startup/callback verification and ordered shutdown (fake SDK/listener)'
