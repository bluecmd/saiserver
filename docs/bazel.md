# Hermetic Bazel / Bzlmod build

The supported build host/target is **Linux x86_64**, using **Bazel 9.3.1**.
Run Bazel through [Bazelisk](https://github.com/bazelbuild/bazelisk): it reads
`.bazelversion` and verifies the downloaded binary against the SHA-256 in
`.bazeliskrc`. Bazel is the only build system; it does not use an installed
Rust/C++ compiler, Thrift, or SAI SDK.

## Build and test

```sh
bazel build //:client //:server
bazel test //...
bazel run //:client -- --help
```

The first build downloads toolchains and builds the C++ standard library;
subsequent builds use ordinary Bazel caching. Every action runs in
`linux-sandbox` without network access (`.bazelrc`). The system tests also need
unprivileged user namespaces and `/dev/net/tun` on the test host.

Locally, the few shell tools Bazel itself needs (Bash/coreutils for its test
harness and rules_rust's bootstrap; see below) come from the host. For a fully
pinned execution environment, use remote execution.

### Remote execution

```sh
bazel test --config=remote //...
```

`--config=remote` runs actions on BuildBuddy (`argocd-apps/apps/buildbuddy`),
uses its cache, and streams the invocation to its UI. The execution platform
`//platforms:remote_linux_x86_64` pins every action's container to the official
Debian image **by digest**, with networking off, so the shell tools are identical
on every run. Tests tagged `no-remote-exec` (the system tests, which need local
kernel features) still run in the local sandbox. The executor pulls the image
from Docker Hub once and then caches it. Anonymous builds are accepted. If
`100.99.0.75` is unreachable, forward the service with
`kubectl -n buildbuddy port-forward svc/buildbuddy 1985:1985` and override the
three endpoints with `grpc://localhost:1985`.

### What is pinned / what “hermetic” covers

- `MODULE.bazel` / `MODULE.bazel.lock` pin the Bzlmod graph.
- `rules_rust 0.75.0` supplies downloaded **Rust 1.94.0**; the Linux tool
  archive SHA-256 values are also explicit in our module.
- `toolchains_llvm_bootstrapped 0.5.9` supplies checksum-pinned **LLVM 21.1.8**,
  linker, libc headers/CRT/link stubs, compiler runtime, libc++, libc++abi and
  libunwind. There is no host C++ compiler or host sysroot discovery.
  The default Linux GNU target uses a glibc 2.28 symbol baseline.
- **Apache Thrift 0.25.0** compiler and the binary/buffered socket runtime are
  built from a checksum-pinned official source release. The release contains
  its generated parser, so flex/bison, configure, CMake and Python are unnecessary.
  The compiler includes C++, Rust and Python generators. The C++ runtime target
  is intentionally the binary/buffered + `TSimpleServer` stack, **not** an
  implementation of every optional Thrift transport (SSL/HTTP/JSON/zlib/etc.).
- **SAI 1.18.1** interface headers come from a checksum-pinned official archive,
  including experimental headers. No vendor binary is downloaded by the build.
- Rust crates are declared with `crate.spec` in `MODULE.bazel`; there is no
  Cargo project. `cargo-bazel-lock.json` commits crate_universe's resolved
  graph and checksums so downstream modules do not repin it, and
  `Cargo.Bazel.lock` (crate_universe's own Cargo-format lock) keeps transitive
  versions stable across repins. Resolution uses a downloaded, isolated
  Cargo/Rust tool set, not a user's Cargo home.
- Target compilation uses `PATH=/nonexistent`. Execution-tool actions have a
  separate, fixed `/usr/bin:/bin` PATH: rules_rust bootstraps its process wrapper
  through a POSIX shell twice and copies three placeholders with Bash/cp. This detail is
  why merely selecting hermetic Rust/LLVM toolchains is not sufficient by itself.
- Bazel itself is pinned by `.bazelversion` plus Bazelisk's SHA-256 check.
  With `--config=remote`, those bootstrap tools come from the digest-pinned
  Debian image; locally they come from the host.
- All configurations fix the locale/timezone, disable stamping and disable
  action network access. Standard test actions, **including test executables
  and subprocesses as well as Bazel's launcher/XML harness**, receive
  `/usr/bin:/bin`; with `--config=remote` these tools are from the pinned image.

**Runtime boundaries:** the host kernel is a prerequisite, not an OS image
produced by this project. Built programs target
glibc rather than being fully static system images. A vendor SDK, switch
configuration, terminal and network are **runtime inputs**, not hermetic build
inputs. This does not claim hermetic execution of ASIC software.

## Public targets

All these labels also work as `@saiserver//:...` from another module. They,
the `//idl` IDL targets and `//bazel:*.bzl` are the public surface; `//src` and
`//tui` targets are visible only inside this repository.

| Target | Kind / purpose |
|---|---|
| `//:client` | Rust `sai-tui` executable |
| `//:client_lib` | Rust library, crate name `sai_tui`; client, commands, UI, counters; re-exports `//:thrift_rust` as `sai_tui::sai_tui` |
| `//:server` | Standalone C++ server, with explicit runtime SDK loader |
| `//:server_lib` | C++ RPC listener/handlers, without a vendor SDK implementation or standalone `main` |
| `//:server_api` | Bounded C++ management backend (`#include "src/tui_rpc.h"`), without the legacy listener/main |
| `//:sai_loader` | Optional SDK-neutral C entrypoint loader, for embedding applications |
| `//:sai_headers` | `CcInfo` for official SAI headers; `#include <sai.h>` etc. |
| `//:thrift_idl` | `thrift_library` (`ThriftInfo`) for `switch_sai.thrift` and its `sai_tui.thrift` include |
| `//:thrift_cpp` | Generated C++ types/services plus the required Thrift runtime |
| `//:thrift_rust` | Freshly generated Rust RPC library, crate name `sai_tui_rpc` |
| `//:thrift_rust_runtime` | Matching Rust `thrift` runtime, preserving trait/crate identity |
| `//:thrift_compiler` | Source-built Thrift compiler |
| `//:thrift_runtime` | Binary/buffered socket C++ Thrift runtime |
| `//:tests` | Every project Bazel test target |

The IDL lives in `//idl`: `@saiserver//idl:sai_tui_thrift` and
`@saiserver//idl:switch_sai_thrift` are the `thrift_library` targets (the
latter inherits the bounded service), and the raw files are exported as
`@saiserver//idl:sai_tui.thrift` and `@saiserver//idl:switch_sai.thrift`.

Rust consumers constructing protocols/serializing these types should depend on
`@saiserver//:thrift_rust_runtime` and import it as `thrift`. Do not independently
regenerate a second runtime from another crate_universe repository: even the
same version can have a different Rust crate identity and incompatible traits.
The downstream test performs real in-memory serialization and constructs a
generated service client using the exported runtime.

The client re-exports the generated `sai_tui_rpc` crate as `sai_tui::sai_tui`,
so both paths name the same Rust types. Depend on `//:thrift_rust` alone to
use the protocol without pulling in Ratatui.

## Downstream Bzlmod projects

A complete, separately tested consumer is in [examples/bazel](../examples/bazel).
It builds both executables, links the actual server library, uses both Rust
libraries, and generates/compiles a new protocol importing our IDL. Run it from
the repository root with:

```sh
(cd examples/bazel && bazel test //... @saiserver//tui:cli_test)
```

For a fully pinned execution environment, another project can reuse
`@saiserver//platforms:remote_linux_x86_64` or define its own digest-pinned
execution platform.

Its `MODULE.bazel` is the starting point:

```starlark
module(name = "my_application")

bazel_dep(name = "saiserver", version = "0.1.0")
bazel_dep(name = "rules_cc", version = "0.2.17")
bazel_dep(name = "rules_rust", version = "0.75.0")
bazel_dep(name = "toolchains_llvm_bootstrapped", version = "0.5.9")

# This module has not been published in the Bazel Central Registry.
# Select the exact commit containing the Bazel support, not a moving branch.
archive_override(
    module_name = "saiserver",
    urls = ["https://github.com/bluecmd/saiserver/archive/<full-commit>.tar.gz"],
    strip_prefix = "saiserver-<full-commit>",
    integrity = "sha256-<base64-archive-sha256>",
)

# rules_rust intentionally accepts toolchain configuration only from the root.
# Its pinned 0.75.0 release contains the 1.94.0 archive checksums.
rust = use_extension("@rules_rust//rust:extensions.bzl", "rust")
rust.toolchain(edition = "2021", versions = ["1.94.0"], rustfmt_version = "1.94.0")
use_repo(rust, "rust_toolchains")
register_toolchains("@rust_toolchains//:all")
```

Replace both placeholders with the published source commit and verified archive
digest; this is not a usable floating URL. A full-commit `git_override` is also
possible, but additionally requires a pinned Git executable in the repository
fetch environment; archives avoid that extra tool. The example's local override is solely for testing this checkout,
not an implicit dependency on a developer machine.

Dependency `.bazelrc` files are **not inherited**. Copy this repository's
[.bazelrc](../.bazelrc) (the example imports it), in particular the hermetic compiler
selection/strict environment and this required Rust/LLVM interoperability flag:

```text
common --repo_env=BAZEL_DO_NOT_DETECT_CPP_TOOLCHAIN=1
build --@toolchains_llvm_bootstrapped//config:experimental_stub_libgcc_s=True
```

Keep the matching `rules_cc` version: 0.2.27 removed an API used by this LLVM
toolchain release. The example is pinned to the verified 0.2.17 combination.
A downstream project may select its own toolchains/platforms, but doing so
changes the tested hermetic configuration; using our libraries alone does not
make an unrelated project's existing host toolchains hermetic.

For a new downstream workspace, generate and commit its module lock once with
`bazel test --lockfile_mode=update //...`; normal builds use frozen locks.

### C++ embedding

```starlark
load("@rules_cc//cc:cc_library.bzl", "cc_library")

cc_library(
    name = "my_sai_application",
    srcs = ["application.cpp"],
    deps = [
        "@saiserver//:server_lib",
        "@saiserver//:sai_headers",
        ":my_checksum_pinned_sdk",  # Or @saiserver//:sai_loader, not both.
    ],
)
```

The legacy listener expects the embedding application to define
`sai_object_id_t gSwitchId` and `std::mutex gFdbMutex`. Initialize the SDK and
set the actual switch ID before starting the RPC server. Register/coordinate
notification callbacks and SDK lifecycle as in the standalone main. The
[consumer](../examples/bazel/consumer.cpp) demonstrates actual library linkage
without starting a listener or touching hardware. Its failing API provider is
**test-only**, never a production default. The bounded `server_api` backend
instead accepts the switch ID explicitly.

Project headers are included by their repository path, e.g.
`#include "src/switch_sai_rpc_server.h"`; generated Thrift headers by file name
(`#include "switch_sai_rpc.h"`), since Thrift's own output includes them that way.
SAI's C headers require `extern "C" { #include <sai.h> }` when used from C++
(write the include on its own line, as in the consumer). A vendor `cc_import`
and all of its link-time dependencies must come from declared pinned artifacts;
do not restore `-L/usr/lib -lsai` or search a local SDK.

### More protocol generation

`@saiserver//bazel:thrift.bzl` follows the `proto_library` pattern:

```starlark
load("@saiserver//bazel:thrift.bzl", "cc_thrift_library", "thrift_library")

thrift_library(
    name = "my_protocol_thrift",
    src = "my_protocol.thrift",  # e.g. include "sai_tui.thrift"
    deps = ["@saiserver//:thrift_idl"],
)

cc_thrift_library(
    name = "my_protocol_cc",
    lib = ":my_protocol_thrift",
    outs = ["my_protocol_types.cpp", "my_protocol_types.h"],
    deps = ["@saiserver//:thrift_cpp"],  # C++ for the included IDL.
)
```

`thrift_library` holds one `.thrift` file and the `thrift_library` targets it
includes; its `ThriftInfo` provider carries the transitive sources and `-I`
directories. `cc_thrift_library` and `rust_thrift_library` generate and compile
bindings, adding the matching Thrift runtime. The Thrift compiler names its
outputs after the file and its services, so `outs` (or `out` for Rust) must
list them. The lower-level `thrift_codegen` rule takes any generator spec. All
of them invoke the pinned compiler directly; there is no shell command or host
Thrift lookup.

## Obtaining binaries and vendor SDK deployment

After `bazel build -c opt //:client //:server` (with or without
`--config=remote`), copy the binaries out of `bazel-bin`:

```sh
cp bazel-bin/tui/sai-tui bazel-bin/src/saiserver /destination/
```

Run/deploy those binaries in the intended terminal/SDK environment. The build
does not import a host SDK.


The Bazel standalone server does not link against `libsai` while building.
It exports five C entrypoint forwarders and loads an SDK **only when started**:

```sh
# Run only in an explicitly prepared switch/SDK environment, never alongside
# SONiC's active SDK instance. Building/testing does not require this command.
SAI_LIBRARY_PATH=/absolute/path/to/libsai.so \
  ./saiserver --no-shell --profile /absolute/path/to/sai.profile
```

The SDK and its dependency closure must be installed for that deployment and
compatible with the SAI 1.18.1 headers. This change is not a new hardware
validation of arbitrary SDK versions. The SDK may impose a newer glibc minimum
than the standalone executable.

Missing/non-absolute paths, load errors or missing required symbols fail closed.
There is no soname search, default SDK, fake implementation or automatic retry.
Loader success **and failure** are cached thread-safely; configure the environment
before the first SAI call and restart to change it. The SDK remains mapped for
process lifetime so returned function tables/callbacks cannot be unmapped.
SDK lifecycle calls and statuses are forwarded, not emulated.
Vendor-specific weak-symbol version banners may be absent with local runtime
loading; `sai_query_api_version` still queries the selected SDK itself.

**C++ exceptions from the SDK.** SAI is a C ABI, so an SDK letting a C++
exception escape a `sai_*` call is an SDK bug. The loader still catches it and
returns `SAI_STATUS_FAILURE`, and if initialization failed the server exits
without running static destructors, since the SDK may have left threads behind.
Catching it is only possible because the process has a **single unwinder**. Our
toolchain links LLVM libunwind statically, while a GCC-built SDK brings
libgcc_s. Two unwinders in one process cannot handle each other's frames, and an
SDK exception used to crash the server instead of being caught. Linking
`//:sai_loader` therefore forces in and exports LLVM libunwind's full
`_Unwind_*` API, so the dynamic linker binds the SDK's, libstdc++'s and
libgcc_s's unwinder calls to it as well. LLVM libunwind is the only unwinder
this toolchain supports, and it implements the same ABI as libgcc_s. See
[`bazel/unwinder.bzl`](../bazel/unwinder.bzl) for the details;
`//tests/system:vs_sdk_exception_test` checks it against SONiC's GCC-built
libsaivs.

This is containment, not a guarantee. LLVM libunwind now also unwinds
exceptions the SDK throws and catches internally. An exception thrown on an SDK
thread still terminates the process, as it would anywhere. An embedder that
links an SDK directly must keep the same arrangement: one unwinder, exported
from the executable.


## System tests against a software SAI

`//tests/system` runs the real `saiserver` and `sai-tui` against SONiC's
virtual-switch SAI, **libsaivs**, as an ordinary `bazel test` (part of `//...`):

```sh
bazel test //tests/system/...
```

`vs_docs_workflows_test` executes every command of the "Explicit workflows" in
[tui.md](tui.md) verbatim and in order, through the CLI, requiring verified
readback for each; `# -> LABEL` comments there bind the returned keys for later
commands. It then removes everything it created and verifies the removals. A
documented example that stops working therefore fails the build.

`vs_fdb_learning_test` covers the notification path: two switch ports are backed
by veth pairs (`lanemap.ini`, `vs_fdb.profile`), the test creates their netdev
host interfaces through the legacy RPC API, injects frames on a veth peer, and
requires the learned entry to reach the server's FDB notification handler and
the getter-verified inventory (and the legacy FDB list). A flush must remove it.
libsaivs learns only on ports with TAP host interfaces, so this test needs
`/dev/net/tun` on the test host.

libsaivs keeps a metadata-validated object model and learns MACs, but it does
**not** forward packets, so these tests cover the management and notification
planes (validation, object references, getters, readback, removal, FDB
events), not data-plane behaviour.

How it runs, without root or a container engine:

- `vs_rootfs` is a Debian trixie userspace from `rules_distroless`, resolved
  from a snapshot.debian.org timestamp (the package-index hashes are pinned in
  `MODULE.bazel.lock`), plus the SONiC `libsaivs`, `libsaimetadata` and
  `libswsscommon` packages. Those are mirrored with provenance in the
  [`sonic-vs-debs-20261028.2`](https://github.com/bluecmd/saiserver/releases/tag/sonic-vs-debs-20261028.2)
  release and pinned by SHA-256.
- The test unpacks the rootfs into `TEST_TMPDIR`; `nsrun` (`nsrun.cc`) then
  chroots into it inside new user, mount, network, PID, IPC and UTS
  namespaces, with only loopback networking.
  This needs unprivileged user namespaces on the test host, so these tests are
  tagged `no-remote-exec`.
- `vs_switch.sh` starts the Redis instance libsaivs insists on and the server
  with `SAI_LIBRARY_PATH` pointing at libsaivs, then runs the test command.

Known libsaivs limitations, pinned so a change is noticed:

- Attributes left at their SAI defaults read back as `NOT_IMPLEMENTED`; the
  server reports them as `unavailable.<name>` (see [server-api.md](server-api.md)).
- ACL table match-field enables that were not set at creation cannot be read,
  and they identify the table, so the ACL workflow fails at its first
  `create acl_table` with `READBACK FAILED`. The test asserts exactly that
  (`--known-unsupported`) and skips the rest of that section.
- A learned MAC seen on another port is not reported as moved (libsaivs keys
  entries by MAC and VLAN; see sonic-net/sonic-sairedis#2114). The FDB test
  asserts the entry stays put, so an upgrade that adds moves is noticed.

To move to newer SONiC packages, download the trixie debs from a successful
`Azure.sonic-buildimage.official.vs` build, attach them with provenance to a new
release, and update the URLs and hashes in `MODULE.bazel`. Changing the Debian
snapshot timestamp needs `--lockfile_mode=update` once.

## Verification and maintenance

Project tests cover 29 Rust unit/integration cases, the existing getter-backed
C++/FDB regressions, 12 fake-only loader scenarios, rustfmt checks and the
libsaivs system tests. All are offline/hardware-free; the CLI tests communicate only over loopback.

A clean native build/test passed with frozen module locks, fetch/downloads disabled,
remote/disk caches disabled, action network disabled, target `PATH=/nonexistent`,
and sandbox access blocked to host `/usr/include`, GCC/G++, the user's
`.cargo`, and the private `.lab` SDK directory. The resulting client/server
SHA-256 values matched the previous build. This verifies the project build
closure, not a reproducible OS image or live SDK initialization.
The separate consumer's C++ and Rust tests also passed, including real Rust
serialization through the exported runtime and the external CLI runfiles test.
The complete suite also passed with `--config=remote` (2,380 remote actions;
the system tests ran locally as tagged). A probe test confirmed that remote
actions run in the pinned Debian image without network access.

For the fully pinned configuration, use `bazel test --config=remote //...`.
An additional native closure probe, after warming repository downloads, is:

```sh
bazel clean
bazel test --nofetch --repository_disable_download --remote_cache= --disk_cache= \
  --sandbox_block_path=/usr/include \
  --sandbox_block_path=/usr/bin/gcc --sandbox_block_path=/usr/bin/g++ //...
(cd examples/bazel && bazel test //...)
```

Locks are frozen (`--lockfile_mode=error`), so repins are deliberate source
edits: review the changes, then verify with `--config=remote`. To change Rust dependencies, edit the `crate.spec` tags in
`MODULE.bazel`, then repin (`CARGO_BAZEL_REPIN=1` re-resolves all crates within
their specs; `CARGO_BAZEL_REPIN=thrift` only that one):

```sh
CARGO_BAZEL_REPIN=1 bazel build --lockfile_mode=update --repo_env=CARGO_BAZEL_REPIN=1 //:client
bazel test //...
(cd examples/bazel && bazel test --lockfile_mode=update //...)
```

Format and lint Starlark with `bazel run //tools:buildifier` (or
`//tools:buildifier.check` to only report), and lint Rust with
`bazel build --config=clippy //...`. Commit both crate_universe locks and both
Bzlmod locks together. Do not use a
repin environment variable during ordinary builds. Changing toolchain/SAI/Thrift
versions also requires updating the explicit archive hashes, regenerating locks,
and repeating the downstream and clean-sandbox checks.
