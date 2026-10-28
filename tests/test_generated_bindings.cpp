// Ensure Cargo's checked-in RPC module is the same pinned IDL/compiler output
// as Bazel's standalone RPC crate, apart from two documented lint attributes.
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>

std::string read_binding(const char* path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error(std::string("cannot read ") + path);
    std::ostringstream result;
    std::string line;
    while (std::getline(input, line)) {
        if (line == "#![allow(clippy::too_many_arguments, clippy::type_complexity, clippy::vec_box, clippy::wrong_self_convention)]" ||
            line == "#![cfg_attr(rustfmt, rustfmt_skip)]") continue;
        result << line << '\n';
    }
    return result.str();
}

int main(int argc, char** argv) {
    try {
        if (argc != 3) throw std::runtime_error("expected generated and checked-in Rust binding paths");
        if (read_binding(argv[1]) != read_binding(argv[2])) {
            std::cerr << "Checked-in Rust bindings differ from Thrift 0.25.0 generation. "
                         "Regenerate tui/src/sai_tui.rs from idl/sai_tui.thrift and preserve the two lint attributes.\n";
            return 1;
        }
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
