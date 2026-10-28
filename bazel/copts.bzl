"""Compiler flags shared by this repository's C++ targets.

These are set per target rather than in .bazelrc because downstream modules
build our libraries without our .bazelrc.
"""

SAISERVER_COPTS = ["-std=c++17"]

# Tests and fakes are warning-clean and always keep their assert()s.
SAISERVER_TEST_COPTS = SAISERVER_COPTS + [
    "-Wall",
    "-Wextra",
    "-Werror",
    "-UNDEBUG",
]
