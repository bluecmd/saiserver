// Lists a saiserver's ports and VLAN membership, like `show interfaces brief`,
// through the generated C++ bindings of the bounded SaiTui API
// (@saiserver//:thrift_cpp, which also brings the Thrift runtime).
//
// Usage: show_interfaces_cpp [HOST [PORT]]   (default: 127.0.0.1 9090)
#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <memory>
#include <string>
#include <vector>

#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/transport/TBufferTransports.h>
#include <thrift/transport/TSocket.h>

#include "SaiTui.h"

namespace {

using Attributes = std::map<std::string, std::string>;

// "-" if the SDK reported no such attribute, "?" if its getter is unsupported.
std::string attribute(const sai_tui::Object& object, const std::string& name) {
    auto it = object.attributes.find(name);
    if (it != object.attributes.end()) return it->second;
    return object.attributes.count("unavailable." + name) ? "?" : "-";
}

std::string admin(const std::string& value) {
    return value == "true" ? "up" : value == "false" ? "down" : value;
}

// sai_port_oper_status_t
std::string oper(const std::string& value) {
    if (value == "1") return "up";
    if (value == "2") return "down";
    if (value == "3") return "testing";
    if (value == "4") return "absent";
    if (value == "-" || value == "?") return value;
    return "unknown";
}

// SAI reports port speed in Mb/s.
std::string speed(const std::string& value) {
    if (value.empty() || value.find_first_not_of("0123456789") != std::string::npos) return value;
    const unsigned long mbps = std::stoul(value);
    return mbps % 1000 == 0 ? std::to_string(mbps / 1000) + "G" : std::to_string(mbps) + "M";
}

// Numeric order for VLAN IDs; anything unparsable sorts last.
unsigned long number(const std::string& value) {
    if (value.empty() || value.find_first_not_of("0123456789") != std::string::npos) return ~0UL;
    return std::stoul(value);
}

void print(const sai_tui::Inventory& inventory) {
    std::vector<const sai_tui::Object*> ports, vlans, members;
    std::map<std::string, std::string> port_of_bridge_port;
    for (const auto& object : inventory.objects) {
        if (object.kind == "port") ports.push_back(&object);
        if (object.kind == "vlan") vlans.push_back(&object);
        if (object.kind == "vlan_member") members.push_back(&object);
        if (object.kind == "bridge_port") port_of_bridge_port[object.key] = attribute(object, "port");
    }

    std::printf("%-14s %-16s %-6s %-6s %-8s %s\n", "Port", "Lanes", "Speed", "Admin", "Oper", "PVID");
    for (const auto* port : ports) {
        std::printf("%-14s %-16s %-6s %-6s %-8s %s\n", port->key.c_str(), attribute(*port, "lanes").c_str(),
                    speed(attribute(*port, "speed")).c_str(), admin(attribute(*port, "admin")).c_str(),
                    oper(attribute(*port, "oper_status")).c_str(), attribute(*port, "pvid").c_str());
    }

    // VLAN key -> tagging mode -> member ports, in port order.
    std::map<std::string, std::map<std::string, std::vector<std::string>>> by_vlan;
    for (const auto* port : ports) {
        for (const auto* member : members) {
            auto bridge_port = port_of_bridge_port.find(attribute(*member, "bridge_port"));
            if (bridge_port == port_of_bridge_port.end() || bridge_port->second != port->key) continue;
            by_vlan[attribute(*member, "vlan")][attribute(*member, "tagging")].push_back(port->key);
        }
    }
    std::sort(vlans.begin(), vlans.end(), [](const sai_tui::Object* a, const sai_tui::Object* b) {
        return number(attribute(*a, "vlan_id")) < number(attribute(*b, "vlan_id"));
    });
    std::printf("\n%-5s %-9s %s\n", "VLAN", "Mode", "Ports");
    for (const auto* vlan : vlans) {
        const auto& modes = by_vlan[vlan->key];
        if (modes.empty()) std::printf("%-5s %-9s %s\n", attribute(*vlan, "vlan_id").c_str(), "-", "-");
        for (const auto& mode : modes) {
            std::string list;
            for (const auto& port : mode.second) list += (list.empty() ? "" : " ") + port;
            std::printf("%-5s %-9s %s\n", attribute(*vlan, "vlan_id").c_str(), mode.first.c_str(), list.c_str());
        }
    }
}

}  // namespace

int main(int argc, char** argv) {
    const std::string host = argc > 1 ? argv[1] : "127.0.0.1";
    const int port = argc > 2 ? std::atoi(argv[2]) : 9090;
    try {
        auto socket = std::make_shared<apache::thrift::transport::TSocket>(host, port);
        auto transport = std::make_shared<apache::thrift::transport::TBufferedTransport>(socket);
        sai_tui::SaiTuiClient client(std::make_shared<apache::thrift::protocol::TBinaryProtocol>(transport));
        transport->open();
        sai_tui::Inventory inventory;
        client.tui_snapshot(inventory);
        print(inventory);
    } catch (const sai_tui::RpcError& e) {
        std::fprintf(stderr, "saiserver error %d: %s\n", e.status, e.message.c_str());
        return 1;
    } catch (const apache::thrift::TException& e) {
        std::fprintf(stderr, "%s:%d: %s\n", host.c_str(), port, e.what());
        return 1;
    }
}
