#!/usr/bin/env bash
# Launcher policy regressions. Only a tiny fake engine is called; no containers,
# network, SDK, host home mount or real engine is used by these tests.
set -euo pipefail
tmp=$(mktemp -d "${TEST_TMPDIR:-/tmp}/bazelw-guards.XXXXXXXX")
trap 'rm -rf -- "$tmp"' EXIT
mkdir -p "$tmp/repo/bazel" "$tmp/real-home" "$tmp/cache"
cp -- "$1" "$tmp/repo/bazelw"
touch "$tmp/repo/bazel/bootstrap.Dockerfile"
ln -s "$tmp/real-home" "$tmp/home-link"

engine="$tmp/fake-engine"
cat > "$engine" <<'ENGINE'
#!/usr/bin/env bash
if [[ ${1:-} == --version ]]; then
    printf 'podman version fake-policy-test\n'
    exit 0
fi
printf 'FAKE_ENGINE_BUILD_SENTINEL\n' >&2
exit 77
ENGINE
chmod +x "$engine"

expect_rejection() {
    local expected=$1
    shift
    if "$@" >"$tmp/output" 2>&1; then
        printf 'unexpected launcher success\n' >&2
        exit 1
    fi
    if ! grep -Fq -- "$expected" "$tmp/output"; then
        printf 'expected diagnostic: %s\n' "$expected" >&2
        cat "$tmp/output" >&2
        exit 1
    fi
}

for flag in '--strategy=Rustc=local' '--strategy_regexp=.*=local' \
            '--spawn_strategy=standalone' '--test_strategy=exclusive' \
            '--experimental_spawn_scheduler'; do
    expect_rejection 'execution-strategy overrides are not allowed' \
        env BAZELW_CONTAINER_ENGINE=/engine-must-not-run \
        bash "$tmp/repo/bazelw" build "$flag" //:client
done

# Native Bazel may be run as root, but bazelw intentionally refuses it.
# Strategy tests above run before that guard. The supported full bootstrap uses
# a non-root user, where this regression also verifies HOME's symlink boundary.
if [[ $(id -u) != 0 ]]; then
    expect_rejection 'must not contain the host home directory' \
        env HOME="$tmp/home-link" BAZELW_CACHE_DIR="$tmp/home-link" \
        BAZELW_CONTAINER_ENGINE="$engine" bash "$tmp/repo/bazelw" build //:client
    [[ ! -e $tmp/real-home/output ]] || {
        printf 'launcher wrote into the rejected home directory\n' >&2; exit 1;
    }

    # Runtime argv is not confused with Bazel options: it reaches our harmless
    # fake build sentinel rather than being rejected as an execution override.
    expect_rejection 'FAKE_ENGINE_BUILD_SENTINEL' \
        env HOME="$tmp/real-home" BAZELW_CACHE_DIR="$tmp/cache" \
        BAZELW_CONTAINER_ENGINE="$engine" bash "$tmp/repo/bazelw" \
        run //:client -- --strategy=application-argument
fi
printf 'bazelw policy guard regressions passed\n'
