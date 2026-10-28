#!/usr/bin/env bash
# Only self-built fake DSOs. No installed SDK, network or hardware.
set -euo pipefail
cd "$(dirname "$0")/../.."
: "${SAI_HEADER_DIR:?set SAI_HEADER_DIR to official SAI inc/}"
build=$(mktemp -d)
trap 'rm -rf "$build"' EXIT
flags=(-std=c++11 -Wall -Wextra -Werror -pedantic -g -pthread
  -I"$SAI_HEADER_DIR" -I"$SAI_HEADER_DIR/experimental" -I"$SAI_HEADER_DIR/../experimental")
"${CXX:-g++}" "${flags[@]}" -shared -fPIC tests/fake_sai.cpp -o "$build/complete.so"
"${CXX:-g++}" "${flags[@]}" -shared -fPIC -DFAKE_SAI_OMIT_LOG_SET tests/fake_sai.cpp -o "$build/incomplete.so"
"${CXX:-g++}" "${flags[@]}" -shared -fPIC tests/fake_sai.cpp tests/server/fake_optional_sai.cpp -o "$build/optional.so"
"${CXX:-g++}" "${flags[@]}" tests/test_sai_dynamic.cpp src/sai_dynamic.cpp -ldl -o "$build/test"
"$build/test" "$build/complete.so" "$build/incomplete.so" "$build/optional.so"
