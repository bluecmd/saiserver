# Hermetic Bazel / Bzlmod build

The supported build host/target is **Linux x86_64**, using **Bazel 9.3.1**.
Use `./bazelw` for the fully pinned bootstrap: it runs Bazel inside the
digest-pinned Linux image defined in [bootstrap.Dockerfile](../bazel/bootstrap.Dockerfile),
including the Bash/coreutils used internally by Bazel/rules_rust. The Bazel
binary itself is SHA-256-pinned. No floating package installation is involved.

Bazel is the only build system. It does not use an installed Rust/C++
compiler, Thrift, or SAI SDK.

## Build and test

```sh
./bazelw build //:client //:server
./bazelw test //...
./bazelw run //:client -- --help
```

The launcher prefers **Podman**, which is tested here. Set
`BAZELW_CONTAINER_ENGINE=docker` to select Docker; that code path is implemented
but has not been locally exercised. Linux sandbox namespaces must work: the
launcher fails rather than falling back, and rejects execution-strategy override
flags. Nested namespaces require relaxed seccomp and proc/sys masking; the
container remains non-root, capability-free, read-only and privately namespaced,
without privileged mode, added capabilities, host networking or device mounts.
Use `--jobs=4` on smaller builders. The first build downloads toolchains and builds the C++
standard library; subsequent builds use ordinary Bazel caching. Network is
needed for the initial **image/repository fetch**, not build actions.

Native `bazel build //:client //:server` and `bazel test //...` also work with
Bazel 9.3.1 (or Bazelisk), but then Bash/coreutils and the compiler executables'
basic Linux userspace come from the host. That is **not** the fully pinned
bootstrap configuration; use `bazelw` or an equivalently pinned execution image
when requiring full build hermeticity.

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
- `bazelw` pins those bootstrap tools, the Linux userspace and Bazel itself in
  its immutable image. The checkout is read-only and only a dedicated build
  cache is writable; no host home, SDK installation or build environment is
  imported. Its build/test commands require `linux-sandbox`.
- All configurations fix the locale/timezone, disable stamping and disable
  action network access. Standard test actions, **including test executables
  and subprocesses as well as Bazel's launcher/XML harness**, receive
  `/usr/bin:/bin`; in full mode these tools are from the pinned image.

**Runtime boundaries:** the host kernel/container engine is a bootstrap
prerequisite, not an OS image produced by this project. Built programs target
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
./bazelw --cwd examples/bazel test //... @saiserver//tui:cli_test
```

The launcher always defaults to the checkout root; use `--cwd` for a nested
workspace even when invoking the script from that directory. For another
project, copy the bootstrap Dockerfile and launcher into that project's checkout,
or use the same pinned execution image in its build infrastructure.

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
fetch environment. The minimal bootstrap avoids that extra tool by using
archives. The example's local override is solely for testing this checkout,
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

The launcher deliberately keeps the checkout read-only, including convenience
symlinks. Outputs live in `BAZELW_CACHE_DIR` (default
`$HOME/.cache/saiserver-bazel-bootstrap`). After building, obtain the host path:

```sh
container_bin=$(./bazelw info bazel-bin)
cache=${BAZELW_CACHE_DIR:-$HOME/.cache/saiserver-bazel-bootstrap}
host_bin="$cache/${container_bin#/cache/}"
cp "$host_bin/tui/sai-tui" ./sai-tui
cp "$host_bin/src/saiserver" ./saiserver
```

Run/deploy those binaries in the intended terminal/SDK environment. The builder
does not import a host SDK or automatically expose host-local RPC listeners.
`bazelw run` can allocate a TTY for interactive runs, but localhost is the
container's network namespace, not the host's.


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


## Verification and maintenance

Project tests cover 29 Rust unit/integration cases, the existing getter-backed
C++/FDB regressions, 12 fake-only loader scenarios, rustfmt and launcher
policy guards (including symlinked HOME and forbidden execution strategies).
All are offline/hardware-free; the CLI tests communicate only over loopback.

A clean native build/test passed with frozen module locks, fetch/downloads disabled,
remote/disk caches disabled, action network disabled, target `PATH=/nonexistent`,
and sandbox access blocked to host `/usr/include`, GCC/G++, the user's
`.cargo`, and the private `.lab` SDK directory. The resulting client/server
SHA-256 values matched the previous build. This verifies the project build
closure, not a reproducible OS image or live SDK initialization.
The separate consumer's C++ and Rust tests also passed, including real Rust
serialization through the exported runtime and the external CLI runfiles test.
The full pinned Podman bootstrap also passed the complete project suite and
separate consumer (including the external CLI test). The consumer rebuilt
2,188 Linux-sandbox actions. Isolation probes confirmed a read-only source,
empty masked `.lab`, no forwarded SDK path, non-root UID/GID and no root-owned
cache files. Docker execution remains untested.

For the fully pinned configuration, repeat with `./bazelw test //...` and
`./bazelw --cwd examples/bazel test //...`. An additional native closure probe,
after warming repository downloads, is:

```sh
bazel clean
bazel test --nofetch --repository_disable_download --remote_cache= --disk_cache= \
  --sandbox_block_path=/usr/include \
  --sandbox_block_path=/usr/bin/gcc --sandbox_block_path=/usr/bin/g++ //...
(cd examples/bazel && bazel test //...)
```

The full-mode launcher freezes locks and mounts source read-only. Maintenance
repins are deliberate source edits: use a writable development checkout (or a
writable copy in the pinned image), review the changes, then verify with the
read-only launcher. To change Rust dependencies, edit the `crate.spec` tags in
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
