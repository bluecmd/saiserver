"""target_compatible_with values shared across packages."""

# The C++ server and loader use Linux-only APIs (dlopen, sigtimedwait, ...).
LINUX = ["@platforms//os:linux"]

# crate_universe is only pinned for x86_64-unknown-linux-gnu.
LINUX_X86_64 = LINUX + ["@platforms//cpu:x86_64"]
