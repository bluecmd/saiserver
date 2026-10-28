"""Thrift IDL libraries and shell-free code generation with the pinned compiler.

Modelled on proto_library / cc_proto_library: a `thrift_library` owns one
.thrift file and its `include` dependencies, and the language macros turn
one into a C++ or Rust library.
"""

load("@rules_cc//cc:cc_library.bzl", "cc_library")
load("@rules_rust//rust:defs.bzl", "rust_library")

ThriftInfo = provider(
    doc = "A Thrift IDL file and everything it includes.",
    fields = {
        "src": "File: the library's own .thrift file.",
        "transitive_srcs": "depset of File: src and all included .thrift files.",
        "include_dirs": "depset of str: directories to pass to the compiler as -I.",
    },
)

def _thrift_library_impl(ctx):
    src = ctx.file.src
    deps = [dep[ThriftInfo] for dep in ctx.attr.deps]
    transitive_srcs = depset([src], transitive = [d.transitive_srcs for d in deps])
    include_dirs = depset([src.dirname], transitive = [d.include_dirs for d in deps])
    return [
        ThriftInfo(src = src, transitive_srcs = transitive_srcs, include_dirs = include_dirs),
        DefaultInfo(files = transitive_srcs),
    ]

thrift_library = rule(
    implementation = _thrift_library_impl,
    attrs = {
        "src": attr.label(allow_single_file = [".thrift"], mandatory = True),
        "deps": attr.label_list(
            providers = [ThriftInfo],
            doc = "thrift_library targets that src `include`s.",
        ),
    },
    provides = [ThriftInfo],
    doc = "One .thrift file plus the thrift_library targets it includes.",
)

def _thrift_codegen_impl(ctx):
    if not ctx.outputs.outs:
        fail("outs must list the generated files")
    out_dir = ctx.outputs.outs[0].dirname
    if any([not (out.dirname + "/").startswith(out_dir + "/") for out in ctx.outputs.outs]):
        fail("the first output's directory must contain all outputs")
    info = ctx.attr.lib[ThriftInfo]
    args = ctx.actions.args()
    args.add_all(["-out", out_dir, "--gen", ctx.attr.language])
    args.add_all(info.include_dirs, before_each = "-I", uniquify = True)
    if ctx.attr.recursive:
        args.add("-r")
    args.add(info.src)
    ctx.actions.run(
        executable = ctx.executable._compiler,
        arguments = [args],
        inputs = info.transitive_srcs,
        outputs = ctx.outputs.outs,
        mnemonic = "ThriftGenerate",
        progress_message = "Generating Thrift %s bindings for %s" % (ctx.attr.language, ctx.label),
        use_default_shell_env = False,
        env = {"LC_ALL": "C", "TZ": "UTC"},
    )
    return [DefaultInfo(files = depset(ctx.outputs.outs))]

thrift_codegen = rule(
    implementation = _thrift_codegen_impl,
    attrs = {
        "lib": attr.label(providers = [ThriftInfo], mandatory = True),
        "language": attr.string(mandatory = True, doc = "Generator spec, e.g. `cpp:no_skeleton` or `rs`."),
        "recursive": attr.bool(default = False, doc = "Also generate code for included files (-r)."),
        "outs": attr.output_list(mandatory = True, doc = "Every generated file. The first one's directory is the output root."),
        "_compiler": attr.label(
            default = Label("@saiserver_thrift//:compiler"),
            executable = True,
            cfg = "exec",
        ),
    },
    doc = "Generate declared files without invoking a shell or installed Thrift.",
)

def cc_thrift_library(name, lib, outs, recursive = False, deps = [], **kwargs):
    """C++ bindings for a thrift_library, compiled against the Thrift runtime.

    Args:
      name: the cc_library name.
      lib: the thrift_library to generate from.
      outs: basenames of the generated .h/.cpp files. The compiler names them
        after the IDL file and its services, so they cannot be inferred.
      recursive: also generate (and compile) code for included files.
      deps: extra cc_library deps, e.g. the cc_thrift_library of an include
        when recursive is False.
      **kwargs: passed to cc_library.
    """
    gen_dir = "_thrift_gen/" + name
    thrift_codegen(
        name = name + "_codegen",
        lib = lib,
        language = "cpp:no_skeleton",
        recursive = recursive,
        outs = [gen_dir + "/" + out for out in outs],
        visibility = kwargs.get("visibility"),
        tags = kwargs.get("tags"),
    )
    cc_library(
        name = name,
        srcs = [gen_dir + "/" + out for out in outs if out.endswith(".cpp")],
        hdrs = [gen_dir + "/" + out for out in outs if out.endswith(".h")],
        strip_include_prefix = gen_dir,
        deps = deps + [Label("@saiserver_thrift//:runtime")],
        **kwargs
    )

def rust_thrift_library(name, lib, out, crate_name = None, deps = [], **kwargs):
    """A Rust crate whose root is the generated module for a thrift_library.

    Args:
      name: the rust_library name.
      lib: the thrift_library to generate from.
      out: the generated module's basename (the IDL basename, snake_cased, .rs).
      crate_name: passed to rust_library.
      deps: extra crate deps; the matching `thrift` runtime crate is added.
      **kwargs: passed to rust_library.
    """
    generated = "_thrift_gen/%s/%s" % (name, out)
    thrift_codegen(
        name = name + "_codegen",
        lib = lib,
        language = "rs",
        outs = [generated],
        visibility = kwargs.get("visibility"),
        tags = kwargs.get("tags"),
    )
    rust_library(
        name = name,
        srcs = [generated],
        crate_root = generated,
        crate_name = crate_name,
        deps = deps + [Label("@saiserver_crates//:thrift")],
        **kwargs
    )
