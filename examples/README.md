# Examples: using saiserver from another Bazel module

This directory is an independent Bzlmod module that depends on saiserver the
way a downstream project would. Its `local_path_override` points at this
checkout so it can test unpublished changes; for production, depend on a
full-commit/integrity-pinned archive instead (see [docs/bazel.md](../docs/bazel.md)).

```sh
bazel build //...
bazel run //:show_interfaces_rust -- 127.0.0.1 9090
```

- `show_interfaces_cpp` / `show_interfaces_rust`: connect to a running
  saiserver and print its ports (lanes, speed, admin/oper state, PVID) and
  VLAN membership, like `show interfaces brief`. They use the generated C++
  bindings (`@saiserver//:thrift_cpp`) and the Rust bindings with their
  matching runtime (`@saiserver//:thrift_rust`, `:thrift_rust_runtime`). Both
  print the same table; `//tests/system:vs_examples_test` in the main
  repository runs them against SONiC's software switch SAI.
- `consumer_thrift` / `consumer_cpp`: a new IDL that includes saiserver's,
  compiled with the exported `thrift_library` and `cc_thrift_library` rules.
- `all_exports`: the executables and libraries a consumer deploys or links.

Downstream `.bazelrc` files are not inherited from dependencies; this one
imports the parent's, which a real consumer would copy.
