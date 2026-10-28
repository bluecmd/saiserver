// FDB learning end to end on libsaivs: frames injected on a port's veth are
// learned by the SAI, reported through the server's FDB notification handler,
// and visible (verified by SAI getters) in the bounded inventory; a flush
// removes them again.
//
// libsaivs does not report MAC moves yet (it keys entries by MAC and VLAN and
// only refreshes them; see sonic-net/sonic-sairedis#2114), so the test pins
// that: the entry must stay on its first port. Update it when that changes.
//
// Expects two switch ports backed by veths eth1 (lanes 1-4) and eth2 (lanes
// 5-8), see vs_fdb.profile and lanemap.ini, and saiserver on 127.0.0.1:9090.
#include <arpa/inet.h>
#include <linux/if_packet.h>
#include <net/ethernet.h>
#include <net/if.h>
#include <sys/socket.h>
#include <unistd.h>

#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <functional>
#include <map>
#include <memory>
#include <string>
#include <thread>
#include <vector>

#include <thrift/TOutput.h>
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/transport/TBufferTransports.h>
#include <thrift/transport/TSocket.h>

#include "switch_sai_rpc.h"

extern "C" {
#include <sai.h>
}

namespace {

using apache::thrift::protocol::TBinaryProtocol;
using apache::thrift::transport::TBufferedTransport;
using apache::thrift::transport::TSocket;
using switch_sai::switch_sai_rpcClient;

constexpr char kMac[] = "02:aa:bb:cc:dd:01";

[[noreturn]] void fail(const std::string& message) {
    std::fprintf(stderr, "FAIL: %s\n", message.c_str());
    std::exit(1);
}

void expect(bool condition, const std::string& message) {
    if (!condition) fail(message);
}

// Polls CHECK until it holds, for up to 10 seconds, calling ACT before each try.
void eventually(const std::string& what, const std::function<void()>& act, const std::function<bool()>& check) {
    const auto deadline = std::chrono::steady_clock::now() + std::chrono::seconds(10);
    while (std::chrono::steady_clock::now() < deadline) {
        act();
        if (check()) return;
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
    }
    fail("timed out waiting for " + what);
}

// Sends one broadcast frame from kMac on IFNAME (a veth peer of a switch port).
void inject(const std::string& ifname) {
    int fd = socket(AF_PACKET, SOCK_RAW | SOCK_CLOEXEC, htons(ETH_P_ALL));
    expect(fd >= 0, "packet socket: " + std::string(std::strerror(errno)));
    sockaddr_ll address{};
    address.sll_family = AF_PACKET;
    address.sll_ifindex = static_cast<int>(if_nametoindex(ifname.c_str()));
    expect(address.sll_ifindex != 0, "no interface " + ifname);
    unsigned char frame[60] = {0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x02, 0xaa, 0xbb, 0xcc, 0xdd, 0x01, 0x88, 0xb5};
    expect(sendto(fd, frame, sizeof(frame), 0, reinterpret_cast<sockaddr*>(&address), sizeof(address)) == sizeof(frame),
           "send on " + ifname + ": " + std::strerror(errno));
    close(fd);
}

struct Switch {
    std::shared_ptr<TSocket> socket = std::make_shared<TSocket>("127.0.0.1", 9090);
    std::shared_ptr<TBufferedTransport> transport = std::make_shared<TBufferedTransport>(socket);
    switch_sai_rpcClient client{std::make_shared<TBinaryProtocol>(transport)};

    Switch() {
        const auto deadline = std::chrono::steady_clock::now() + std::chrono::seconds(60);
        apache::thrift::TOutput::instance().setOutputFunction([](const char*) {});  // Startup retries.
        for (;;) {
            try {
                transport->open();
                return;
            } catch (const apache::thrift::TException&) {
                if (std::chrono::steady_clock::now() > deadline) fail("saiserver did not start listening");
                std::this_thread::sleep_for(std::chrono::milliseconds(200));
            }
        }
    }

    std::vector<sai_tui::Object> objects(const std::string& kind) {
        sai_tui::Inventory inventory;
        client.tui_snapshot(inventory);
        std::vector<sai_tui::Object> out;
        for (const auto& object : inventory.objects)
            if (object.kind == kind) out.push_back(object);
        return out;
    }

    // The learned entry for kMac, if any: its bridge port's port, else "".
    std::string learned_on() {
        for (const auto& fdb : objects("fdb")) {
            if (fdb.attributes.at("mac") != kMac) continue;
            sai_tui::Object bridge_port;
            client.tui_get(bridge_port, "bridge_port", fdb.attributes.at("bridge_port"));
            return bridge_port.attributes.at("port");
        }
        return "";
    }

    bool legacy_has_entry() {
        switch_sai::sai_thrift_attribute_list_t entries;
        client.sai_thrift_get_fdb_entries(entries);
        for (const auto& entry : entries.attr_list)
            if (entry.value.fdb_values.thrift_fdb_entry.mac_address == kMac) return true;
        return false;
    }
};

}  // namespace

int main() {
    Switch sw;
    std::map<std::string, std::string> port_by_lanes;
    for (const auto& port : sw.objects("port")) port_by_lanes[port.attributes.at("lanes")] = port.key;
    expect(port_by_lanes.size() == 2, "expected the lane map's two ports, got " + std::to_string(port_by_lanes.size()));
    const std::string eth1 = port_by_lanes.at("1,2,3,4"), eth2 = port_by_lanes.at("5,6,7,8");

    // libsaivs listens on a port's veth once it has a netdev host interface,
    // as SONiC creates for every port; only the legacy API can create those.
    int index = 0;
    for (const auto& port : {eth1, eth2}) {
        std::vector<switch_sai::sai_thrift_attribute_t> attrs(3);
        attrs[0].id = SAI_HOSTIF_ATTR_TYPE;
        attrs[0].value.s32 = SAI_HOSTIF_TYPE_NETDEV;
        attrs[1].id = SAI_HOSTIF_ATTR_OBJ_ID;
        attrs[1].value.oid = std::strtoll(port.c_str(), nullptr, 0);
        attrs[2].id = SAI_HOSTIF_ATTR_NAME;
        attrs[2].value.chardata = "Ethernet" + std::to_string(4 * index++);
        expect(sw.client.sai_thrift_create_hostif(attrs) != 0, "create hostif for port " + port);
        sai_tui::Object out;
        sw.client.tui_set(out, "port", port, {{"admin", "true"}});
        expect(out.attributes.at("admin") == "true", "port " + port + " admin readback");
    }

    eventually("learning on eth1", [] { inject("peer-eth1"); }, [&] { return sw.learned_on() == eth1; });
    expect(sw.legacy_has_entry(), "learned entry missing from the legacy FDB list");
    std::printf("learned %s on port %s\n", kMac, eth1.c_str());

    for (int i = 0; i < 10; ++i) {
        inject("peer-eth2");
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    expect(sw.learned_on() == eth1, "libsaivs now reports MAC moves: assert the move to " + eth2 + " instead");
    std::printf("known libsaivs limitation: no move to port %s\n", eth2.c_str());

    expect(sw.client.sai_thrift_flush_fdb_entries({}) == SAI_STATUS_SUCCESS, "flush FDB");
    eventually("the flush to remove the entry", [] {}, [&] { return sw.learned_on().empty() && !sw.legacy_has_entry(); });
    std::printf("PASS: FDB learn and flush through SAI notifications\n");
}
