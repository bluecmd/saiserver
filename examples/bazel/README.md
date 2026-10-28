# Separate Bzlmod consumer smoke test

From this directory:

```sh
bazel test //...
```

This is an independent root module, not a package in the parent workspace.
Its local override points at the current checkout so it can test unpublished
changes; replace it with a full-commit/integrity-pinned override for production.

- `cpp_consumer_test` links the actual server implementation, SAI headers and
  generated protocol, but never starts SAI or opens a listener.
- `rust_consumer_test` performs in-memory serialization and constructs a service
  client using the public bindings and matching exported Rust Thrift runtime.
- `consumer_protocol` imports the upstream IDL; `consumer_cpp` compiles it.
- `all_exports` also builds the real client and SDK-neutral server executables.

The C++ test API provider is deliberately unsupported/test-only, not a substitute
for a production SDK. See [docs/bazel.md](../../docs/bazel.md) for the exported
labels, hermeticity boundary, toolchain requirements and runtime SDK setup.
