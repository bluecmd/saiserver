#!/usr/bin/env bash
# Unpacks the Debian+libsaivs rootfs and runs a command against saiserver on
# libsaivs inside unprivileged namespaces (see nsrun.cc and vs_switch.sh).
# Usage: vs_test.sh NSRUN ROOTFS_TAR SAISERVER SAI_TUI SWITCH_SH PROFILE DBCONFIG
#        [--bind RLOCATIONPATH:/DST]... -- COMMAND [ARGS...]   (all rlocation paths)
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
r() { rlocation "$1" || { echo "missing runfile $1" >&2; exit 1; }; }
nsrun=$(r "$1"); rootfs_tar=$(r "$2")
binds=(--bind "$(r "$3"):/systest/bin/saiserver" --bind "$(r "$4"):/systest/bin/sai-tui"
       --bind "$(r "$5"):/systest/vs_switch.sh" --bind "$(r "$6"):/systest/vs.profile"
       --bind "$(r "$7"):/systest/database_config.json")
shift 7
while [[ $1 == --bind ]]; do
    binds+=(--bind "$(r "${2%%:*}"):${2#*:}")
    shift 2
done
[[ $1 == -- ]] || { echo "expected -- COMMAND" >&2; exit 2; }
shift

rootfs=$TEST_TMPDIR/rootfs
mkdir -p "$rootfs"
tar -xf "$rootfs_tar" -C "$rootfs"
exec "$nsrun" "$rootfs" "${binds[@]}" -- /bin/bash /systest/vs_switch.sh "$@"
