"""Link options giving a process that loads a vendor SAI SDK a single unwinder.

Why this is needed: C++ exceptions are unwound by an "unwinder" implementing
the Itanium `_Unwind_*` ABI, and each frame's personality routine (libstdc++'s
or libc++abi's `__gxx_personality_v0`) calls back into it with an opaque
context. Our hermetic toolchain links LLVM libunwind statically into every
binary. A vendor SDK built with GCC brings libstdc++ and libgcc_s, a second,
dynamically linked unwinder. When an SDK exception is thrown, the two mix:
libgcc_s's unwinder hands its context to our personality routine, which reads
it with LLVM's layout (or the reverse), and the process crashes in the
unwinder instead of reaching the loader's `catch (...)` that turns SDK
exceptions into `SAI_STATUS_FAILURE`.

Why LLVM libunwind, the one already in our binary: it is the unwinder our
toolchain supports (it cannot link libgcc_s dynamically), and it implements the
same `_Unwind_*` ABI as libgcc_s, being designed as a drop-in replacement for
it. Exporting it from the executable makes the dynamic linker bind every
`_Unwind_*` reference in the process to it, including libstdc++'s and
libgcc_s's own, because the executable is searched before the libraries the
SDK loads. One unwinder then walks every frame, whichever compiler produced it.

Why the whole API, not just what we call: a static archive contributes only
the functions the binary itself references. libstdc++'s personality also calls
e.g. `_Unwind_GetIPInfo` and `_Unwind_GetRegionStart`; if those are missing from
the executable they bind to libgcc_s, which misreads LLVM's context, and the
throw ends in `std::terminate`. So every entry point both unwinders provide is
forced into the link (`--undefined`) and exported. libgcc_s's remaining exports
(`__register_frame_info` and variants) are a legacy frame registry for objects
without `.eh_frame_hdr`; LLVM libunwind finds frames via `dl_iterate_phdr`.

Regression: //tests/system:vs_sdk_exception_test (SONiC's GCC-built libsaivs
throwing out of `sai_api_initialize`).
"""

# Entry points exported by both libgcc_s.so.1 and LLVM libunwind (x86-64).
_UNWIND_API = [
    "__deregister_frame",
    "__register_frame",
    "_Unwind_Backtrace",
    "_Unwind_DeleteException",
    "_Unwind_FindEnclosingFunction",
    "_Unwind_Find_FDE",
    "_Unwind_ForcedUnwind",
    "_Unwind_GetCFA",
    "_Unwind_GetDataRelBase",
    "_Unwind_GetGR",
    "_Unwind_GetIP",
    "_Unwind_GetIPInfo",
    "_Unwind_GetLanguageSpecificData",
    "_Unwind_GetRegionStart",
    "_Unwind_GetTextRelBase",
    "_Unwind_RaiseException",
    "_Unwind_Resume",
    "_Unwind_Resume_or_Rethrow",
    "_Unwind_SetGR",
    "_Unwind_SetIP",
]

SHARED_UNWINDER_LINKOPTS = ["-Wl,--undefined=" + symbol for symbol in _UNWIND_API] + [
    "-Wl,--export-dynamic-symbol=" + symbol
    for symbol in _UNWIND_API
]
