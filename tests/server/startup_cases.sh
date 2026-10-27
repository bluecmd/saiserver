#!/usr/bin/env bash
# Startup/shutdown cases for a built startup_test binary (fake SDK/listener).
# Shared by tests/server/run.sh and Bazel's //tests:startup_test.
set -euo pipefail
: "${1:?usage: startup_cases.sh STARTUP_TEST_BINARY}"
startup_test=$1
opts=(--interface-address --interface-address-static-ipv6-no-dad --interface-address-allow-unpoliced-cpu)
FAKE_STARTUP_MODE=disabled timeout 10 "$startup_test" --no-shell
FAKE_STARTUP_MODE=enabled timeout 10 "$startup_test" "${opts[@]}"
FAKE_STARTUP_MODE=unregister-unsupported timeout 10 "$startup_test" "${opts[@]}"
FAKE_STARTUP_MODE=enabled timeout 10 "$startup_test" --interface-address --interface-address-static-ipv6-no-dad --interface-address-policer 8000
expect_failure() {
  local rc=0
  "$@" || rc=$?
  if [[ $rc != 1 ]]; then echo "Expected exit 1, got $rc: $*" >&2; exit 1; fi
}
for mode in bad-callback cleanup-fail rollback-fail remove-fail uninit-fail; do
  expect_failure env FAKE_STARTUP_MODE="$mode" timeout 10 "$startup_test" "${opts[@]}"
done
expect_failure "$startup_test" --interface-address
expect_failure "$startup_test" --interface-address --interface-address-static-ipv6-no-dad
expect_failure "$startup_test" --interface-address --interface-address-allow-unpoliced-cpu
expect_failure "$startup_test" --interface-address-policer 8000
expect_failure "$startup_test" --interface-address --interface-address-static-ipv6-no-dad --interface-address-policer -1
expect_failure "$startup_test" --interface-address --interface-address-static-ipv6-no-dad --interface-address-policer 18446744073709551616
echo 'PASS real CLI/startup/callback verification and ordered shutdown (fake SDK/listener)'
