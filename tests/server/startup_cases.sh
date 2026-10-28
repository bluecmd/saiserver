#!/usr/bin/env bash
# Startup/shutdown cases for the startup_test binary (fake SDK/listener).
# --- begin runfiles.bash initialization v3 ---
# Copy-pasted from the Bazel Bash runfiles library v3.
set -uo pipefail; set +e; f=bazel_tools/tools/bash/runfiles/runfiles.bash
# shellcheck disable=SC1090
source "${RUNFILES_DIR:-/dev/null}/$f" 2>/dev/null || \
  source "$(grep -sm1 "^$f " "${RUNFILES_MANIFEST_FILE:-/dev/null}" | cut -f2- -d' ')" 2>/dev/null || \
  source "$0.runfiles/$f" 2>/dev/null || \
  source "$(grep -sm1 "^$f " "$0.runfiles_manifest" | cut -f2- -d' ')" 2>/dev/null || \
  source "$(grep -sm1 "^$f " "$0.exe.runfiles_manifest" | cut -f2- -d' ')" 2>/dev/null || \
  { echo>&2 "ERROR: cannot find $f"; exit 1; }; f=; set -e
# --- end runfiles.bash initialization v3 ---
set -euo pipefail
startup_test=$(rlocation "${1:?usage: startup_cases.sh STARTUP_TEST_RLOCATIONPATH}")
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
