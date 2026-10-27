"""Shell-free Thrift generation using the pinned, source-built compiler."""

def _thrift_codegen_impl(ctx):
    if not ctx.outputs.outs:
        fail("outs must list the generated files")
    out_dir = ctx.outputs.outs[0].dirname
    if any([out.dirname != out_dir for out in ctx.outputs.outs]):
        fail("all outputs must share a directory")
    args = ctx.actions.args()
    args.add_all(["-out", out_dir, "--gen", ctx.attr.language])
    dirs = {f.dirname: True for f in ctx.files.includes + [ctx.file.src]}
    for directory in sorted(dirs.keys()):
        args.add_all(["-I", directory])
    if ctx.attr.recursive:
        args.add("-r")
    args.add(ctx.file.src)
    ctx.actions.run(
        executable = ctx.executable._compiler,
        arguments = [args],
        inputs = depset(ctx.files.includes + [ctx.file.src]),
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
        "src": attr.label(allow_single_file = [".thrift"], mandatory = True),
        "includes": attr.label_list(allow_files = [".thrift"]),
        "language": attr.string(mandatory = True),
        "recursive": attr.bool(default = False),
        "outs": attr.output_list(mandatory = True),
        "_compiler": attr.label(
            default = Label("@saiserver_thrift//:compiler"),
            executable = True,
            cfg = "exec",
        ),
    },
    doc = "Generate declared files without invoking a shell or installed Thrift.",
)
