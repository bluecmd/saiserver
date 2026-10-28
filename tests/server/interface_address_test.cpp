#include "src/interface_address.h"
#include <arpa/inet.h>
#include <algorithm>
#include <atomic>
#include <cassert>
#include <chrono>
#include <condition_variable>
#include <cstring>
#include <functional>
#include <iostream>
#include <map>
#include <thread>

#include "tests/server/fake_sdk.h"

using namespace fake_sdk;
namespace {
void packet_tests() {
    auto v4 = target("192.0.2.1"), v6 = target("2001:db8:101::1");
    Bytes p = arp(v4); auto r = reply(v4, p);
    assert(r.size() == 60 && be16(r, 20) == 2);
    assert(std::equal(client.begin(), client.end(), r.begin()));
    assert(std::equal(router.begin(), router.end(), r.begin() + 6));
    assert(std::equal(v4.ip.begin(), v4.ip.begin() + 4, r.begin() + 28));
    assert(std::equal(p.begin() + 28, p.begin() + 32, r.begin() + 38));
    for (size_t off : {size_t(12), size_t(14), size_t(16), size_t(18), size_t(19), size_t(20), size_t(22), size_t(38)}) {
        auto bad = p; bad[off] ^= 1; assert(reply(v4, bad).empty());
    }
    for (size_t n = 0; n < 42; ++n) assert(ia::make_reply(v4, p.data(), n).empty());
    auto bad = p; bad[6] |= 1; assert(reply(v4, bad).empty());
    bad = p; std::fill(bad.begin() + 6, bad.begin() + 12, 0); assert(reply(v4, bad).empty());
    bad = p; bad[0] = 2; assert(reply(v4, bad).empty());
    bad = p; put16(bad, 12, 0x8100); assert(reply(v4, bad).empty());
    bad = p; bad.resize(2049); assert(reply(v4, bad).empty());
    bad = p; std::fill(bad.begin() + 28, bad.begin() + 32, 0); assert(!reply(v4, bad).empty()); // ARP probe.
    p = ns(v6); r = reply(v6, p);
    assert(r.size() == 86 && r[54] == 136 && r[58] == 0xe0 && r[21] == 255 && checksum(r) == 0);
    assert(std::equal(v6.ip.begin(), v6.ip.end(), r.begin() + 22));
    assert(std::equal(p.begin() + 22, p.begin() + 38, r.begin() + 38));
    assert(r[78] == 2 && r[79] == 1 && std::equal(router.begin(), router.end(), r.begin() + 80));
    // Ordinary unicast NS also works and missing SLLA is permitted.
    auto unicast = p; std::copy(v6.ip.begin(), v6.ip.end(), unicast.begin() + 38);
    std::copy(router.begin(), router.end(), unicast.begin()); fix_checksum(unicast); assert(!reply(v6, unicast).empty());
    assert(!reply(v6, ns(v6, false, false)).empty());
    for (size_t n = 0; n < p.size(); ++n) assert(ia::make_reply(v6, p.data(), n).empty());
    for (size_t off : {size_t(0), size_t(12), size_t(18), size_t(20), size_t(21), size_t(54), size_t(55), size_t(56), size_t(62), size_t(79), size_t(80)}) {
        bad = p; bad[off] ^= 1; assert(reply(v6, bad).empty());
    }
    bad = p; bad[14] = 0x40; assert(reply(v6, bad).empty());
    bad = p; bad[20] = 44; assert(reply(v6, bad).empty()); // No atomic or ordinary fragments.
    bad = p; bad[20] = 0; assert(reply(v6, bad).empty()); // No extension traversal.
    bad = p; bad[79] = 0; fix_checksum(bad); assert(reply(v6, bad).empty());
    bad = p; bad[79] = 2; fix_checksum(bad); assert(reply(v6, bad).empty());
    bad = p; bad[80] ^= 2; fix_checksum(bad); assert(reply(v6, bad).empty()); // SLLA vs Ethernet.
    bad = p; bad[22] = 255; fix_checksum(bad); assert(reply(v6, bad).empty());
    bad = p; assert(inet_pton(AF_INET6, "::1", bad.data() + 22) == 1); fix_checksum(bad); assert(reply(v6, bad).empty());
    bad = p; assert(inet_pton(AF_INET6, "::ffff:192.0.2.1", bad.data() + 22) == 1); fix_checksum(bad); assert(reply(v6, bad).empty());
    bad = p; bad[38] ^= 1; fix_checksum(bad); assert(reply(v6, bad).empty());
    bad = p; bad.insert(bad.end(), p.begin() + 78, p.end()); put16(bad, 18, 40); fix_checksum(bad); assert(reply(v6, bad).empty()); // Duplicate SLLA.
    bad = p; bad[78] = 99; fix_checksum(bad); assert(!reply(v6, bad).empty()); // Unknown bounded options skipped.
    bad = p; bad.resize(54 + 25); put16(bad, 18, 25); fix_checksum(bad); assert(reply(v6, bad).empty());
    p = ns(v6, true, false); r = reply(v6, p);
    assert(r.size() == 86 && r[58] == 0xa0 && checksum(r) == 0);
    const uint8_t eth[] = {0x33,0x33,0,0,0,1}; assert(std::equal(eth, eth + 6, r.begin()));
    assert(r[38] == 255 && r[39] == 2 && r[53] == 1);
    assert(reply(v6, ns(v6, true, true)).empty()); // DAD forbids any SLLA.
    bad = p; std::copy(v6.ip.begin(), v6.ip.end(), bad.begin() + 38);
    std::copy(router.begin(), router.end(), bad.begin()); fix_checksum(bad); assert(reply(v6, bad).empty());
    // Deterministic malformed-packet sweep for length/option/checksum boundaries.
    uint32_t seed = 12345;
    for (unsigned i = 0; i < 5000; ++i) {
        seed = seed * 1664525 + 1013904223; bad = ns(v6); bad[seed % bad.size()] ^= uint8_t(seed >> 16);
        (void)reply(v6, bad);
    }
}
void setup_tests() {
    f.reset(); ia::Options disabled; ia::Sdk none; ia::start(sw, disabled, none, hardware);
    assert(!ia::status().running && f.creates == 0); error([] { ia::create(sw, attrs(1)); }, SAI_STATUS_NOT_SUPPORTED);
    auto o = options(); o.allow_unpoliced_cpu = false; error([&] { start(o); }); assert(f.creates == 0);
    error([&] { ia::start(sw, options(), none, hardware); }, SAI_STATUS_NOT_SUPPORTED);
    f.nodes.at(sw).attrs[SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY].ptr = nullptr; error([] { start(); }); assert(f.creates == 0);
    f.reset(); f.enumeration = false; error([] { start(); }); assert(f.creates == 0);
    f.reset(); f.capability = false; error([] { start(); }); assert(f.creates == 0);
    f.reset(); f.hostif.send_hostif_packet = nullptr; error([] { start(); }); assert(f.creates == 0);
    for (auto type : {SAI_HOSTIF_TRAP_TYPE_ARP_REQUEST, SAI_HOSTIF_TRAP_TYPE_IPV6_NEIGHBOR_DISCOVERY}) {
        f.reset(); f.add(9000, SAI_OBJECT_TYPE_HOSTIF_TRAP); f.s32(9000, SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE, type);
        error([] { start(); }, SAI_STATUS_ITEM_ALREADY_EXISTS); assert(f.nodes.count(9000) && f.creates == 0 && f.removes == 0);
    }
    for (unsigned step = 1; step <= 5; ++step) {
        f.reset(); f.fail_create = step; error([] { start(); });
        assert(!ia::status().running && !ia::status().trap_group && f.owned() == 0); ia::stop();
    }
    f.reset(); f.fail_get = 10001; error([] { start(); }); assert(f.owned() == 0); // Readback failure rolls back.
    f.reset(); f.fail_create = 5; f.fail_remove = 10002;
    error([] { start(); }); auto state = ia::status();
    assert(!state.running && state.tables[0] == 10002 && state.traps[0] == 10001 && state.trap_group == 10000 && !state.traps[1]);
    error([] { start(); }, SAI_STATUS_OBJECT_IN_USE); error([] { ia::stop(); });
    f.fail_remove = 0; ia::stop(); assert(f.owned() == 0 && !ia::status().trap_group);
    // Borrowed policer survives stop; no existing state is changed.
    f.reset(); f.add(8000, SAI_OBJECT_TYPE_POLICER); o = options(); o.policer = 8000; o.allow_unpoliced_cpu = false;
    start(o); assert(f.owned() == 5); error([] { start(); });
    auto group = ia::status().trap_group; assert(f.nodes.at(group).attrs.at(SAI_HOSTIF_TRAP_GROUP_ATTR_POLICER).oid == 8000);
    ia::stop(); assert(f.nodes.count(8000) && f.owned() == 0);
    for (unsigned index = 0; index < 5; ++index) {
        f.reset(); start(); f.fail_remove = 10000 + index; error([] { ia::stop(); });
        assert(!ia::status().running && f.nodes.count(f.fail_remove)); f.fail_remove = 0; ia::stop(); assert(f.owned() == 0);
    }
}
void address_tests() {
    f.reset(); f.access(1); f.access(2); start();
    auto a = ia::create(sw, attrs(1)); assert(a.key == "0x3e9@192.0.2.1/24" && a.attributes.at("address") == "192.0.2.1/24");
    assert(a.attributes.at("observation_source") == "software-responder");
    assert(ia::get(sw, "1001@192.0.2.1/24").key == a.key); error([] { ia::create(sw, attrs(1)); }, SAI_STATUS_ITEM_ALREADY_EXISTS);
    error([] { ia::create(sw, attrs(1, "192.0.2.1/32")); });
    auto b = ia::create(sw, attrs(2)); assert(a.key != b.key); // Same IP isolated in distinct VLANs is permitted.
    assert(ia::list(sw).size() == 2);
    auto v6 = ia::create(sw, attrs(1, "2001:0db8:0:0::1234/64"));
    assert(v6.key == "0x3e9@2001:db8::1234/64" && v6.attributes.at("dad") == "static-no-dad");
    for (const char* ip : {"192.0.2.1", "192.0.2.1/33", "2001:db8::1/129", "192.0.2.1/-1", "::/0", "::1/128", "ff02::1/64", "::ffff:192.0.2.1/128", "0.0.0.0/24", "127.0.0.1/8", "224.0.0.1/24", "192.0.2.1/24/junk"})
        error([&] { ia::create(sw, attrs(1, ip)); });
    auto wrong = attrs(1); wrong["extra"] = "x"; error([&] { ia::create(sw, wrong); });
    wrong = attrs(1, "192.0.2.3/24"); wrong["ingress_port"] = "202"; error([&] { ia::create(sw, wrong); });
    error([&] { ia::get(sw + 1, a.key); }); error([] { ia::get(sw, "bad"); });
    // Getter errors are not invented hardware observations; stale addresses remain removable.
    { std::lock_guard<std::mutex> l(hardware); f.u16(201, SAI_PORT_ATTR_PORT_VLAN_ID, 102); }
    error([&] { ia::get(sw, a.key); }); ia::remove(sw, a.key); error([&] { ia::get(sw, a.key); }, SAI_STATUS_ITEM_NOT_FOUND);
    ia::remove(sw, v6.key); ia::remove(sw, b.key); assert(ia::list(sw).empty());
    ia::stop(); f.reset(); f.access(1); auto o = options(); o.static_ipv6_no_dad = false; start(o);
    error([] { ia::create(sw, attrs(1, "2001:db8::1/64")); }, SAI_STATUS_NOT_SUPPORTED); ia::stop();
    // Each unsupported/ambiguous topology rejects address activation.
    for (unsigned test = 0; test < 10; ++test) {
        f.reset(); f.access(1);
        switch (test) {
        case 0: f.u16(201, SAI_PORT_ATTR_PORT_VLAN_ID, 102); break;
        case 1: f.s32(3001, SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE, SAI_VLAN_TAGGING_MODE_TAGGED); break;
        case 2: f.oid(4001, SAI_BRIDGE_PORT_ATTR_PORT_ID, 202); break;
        case 3: f.s32(1001, SAI_ROUTER_INTERFACE_ATTR_TYPE, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT); break;
        case 4: f.nodes.at(1001).attrs[SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS].mac[0] = 1; break;
        case 5: f.nodes.erase(3001); break;
        case 6: f.nodes.emplace(3999, f.nodes.at(3001)); break;
        case 7: f.flag(1001, SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE, false); break;
        case 8: f.s32(5000, SAI_BRIDGE_ATTR_TYPE, SAI_BRIDGE_TYPE_1D); break;
        case 9: f.fail_get = 1001; break;
        }
        start(); error([] { ia::create(sw, attrs(1)); }); assert(ia::status().addresses == 0); ia::stop();
    }
}
void worker_tests() {
    f.reset(); f.access(1); f.access(2); start();
    auto a = ia::create(sw, attrs(1)); ia::create(sw, attrs(2, "198.51.100.1/24"));
    ia::create(sw, attrs(1, "2001:db8:101::1/64"));
    auto state = ia::status(); auto p = arp(target("192.0.2.1")); inject_reliably(p, 201, state.traps[0]); wait_sent(1);
    assert(f.sent[0].first == 201 && be16(f.sent[0].second, 20) == 2);
    inject_reliably(ns(target("2001:db8:101::1")), 201, state.traps[1]); wait_sent(2); assert(f.sent[1].second[58] == 0xe0);
    inject_reliably(ns(target("2001:db8:101::1"), true, false), 201, state.traps[1]); wait_sent(3); assert(f.sent[2].second[58] == 0xa0);
    auto rejected = ia::status().rejected;
    for (auto port : {sai_object_id_t(202), sai_object_id_t(999)}) inject_reliably(p, port, state.traps[0]);
    inject_reliably(p, 201, state.traps[1]); inject_reliably(p, 201, 99999);
    auto tagged = p; put16(tagged, 12, 0x8100); inject_reliably(tagged, 201, state.traps[0]);
    wait_stat([&](const ia::Status& s) { return s.rejected >= rejected + 5; }); assert(f.sent.size() == 3);
    auto drops = ia::status().dropped; inject(p, 201, state.traps[0], sw + 1); inject(p, 201, state.traps[0], sw, true);
    inject(p, 0, state.traps[0]); assert(ia::status().dropped >= drops + 3);
    sai_attribute_t duplicate[3]{}; duplicate[0].id = duplicate[1].id = SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT;
    duplicate[0].value.oid = duplicate[1].value.oid = 201; duplicate[2].id = SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID; duplicate[2].value.oid = state.traps[0];
    ia::packet_callback()(sw, p.size(), p.data(), 3, duplicate); assert(ia::status().dropped >= drops + 4);
    // Stale PVID and stale MAC cannot elicit replies, and errors are observable.
    auto errors = ia::status().errors;
    { std::lock_guard<std::mutex> l(hardware); f.u16(201, SAI_PORT_ATTR_PORT_VLAN_ID, 102); }
    inject_reliably(p, 201, state.traps[0]); wait_stat([&](const ia::Status& s) { return s.errors > errors; }); assert(f.sent.size() == 3);
    { std::lock_guard<std::mutex> l(hardware); f.u16(201, SAI_PORT_ATTR_PORT_VLAN_ID, 101); f.nodes.at(1001).attrs[SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS].mac[5] = 2; }
    errors = ia::status().errors; inject_reliably(p, 201, state.traps[0]); wait_stat([&](const ia::Status& s) { return s.errors > errors; }); assert(f.sent.size() == 3);
    ia::remove(sw, a.key); ia::stop();
    inject(p, 201, state.traps[0]); assert(!ia::status().running && f.owned() == 0);
    // All 32 access VLANs (101..132), both families, plus a direct 10G port RIF.
    f.reset(); for (unsigned n = 1; n <= 33; ++n) f.access(n);
    f.s32(1033, SAI_ROUTER_INTERFACE_ATTR_TYPE, SAI_ROUTER_INTERFACE_TYPE_PORT); f.oid(1033, SAI_ROUTER_INTERFACE_ATTR_PORT_ID, 233);
    start();
    for (unsigned n = 1; n <= 33; ++n) {
        ia::create(sw, attrs(n, "10.0." + std::to_string(n) + ".1/24"));
        ia::create(sw, attrs(n, "2001:db8:" + std::to_string(n) + "::1/64"));
    }
    assert(ia::status().addresses == 66);
    state = ia::status();
    for (unsigned n = 1; n <= 33; ++n) {
        inject_reliably(arp(target(("10.0." + std::to_string(n) + ".1").c_str())), 200 + n, state.traps[0]); wait_sent(2*n - 1);
        inject_reliably(ns(target(("2001:db8:" + std::to_string(n) + "::1").c_str())), 200 + n, state.traps[1]); wait_sent(2*n);
    }
    ia::stop(); assert(f.owned() == 0);
    // Explicit send failure is retained in observable diagnostics, not counted as success.
    f.reset(); f.access(1); start(); ia::create(sw, attrs(1)); state = ia::status(); f.send_error = true;
    inject_reliably(p, 201, state.traps[0]); wait_stat([&](const ia::Status& s) { return s.errors > state.errors; });
    assert(f.sent.empty() && ia::status().last_status == SAI_STATUS_NOT_SUPPORTED && !ia::status().running);
    error([] { ia::create(sw, attrs(1, "192.0.2.3/24")); }, SAI_STATUS_NOT_SUPPORTED);
    error([] { ia::get(sw, "1001@192.0.2.1/24"); }, SAI_STATUS_NOT_SUPPORTED);
    error([] { ia::list(sw); }, SAI_STATUS_NOT_SUPPORTED);
    // A fault must not strand addresses: removal still clears them so that
    // topology mutations are no longer blocked.
    ia::remove(sw, "1001@192.0.2.1/24"); assert(ia::status().addresses == 0);
    error([] { ia::remove(sw, "1001@192.0.2.1/24"); }, SAI_STATUS_ITEM_NOT_FOUND); ia::stop();
}
void bounded_queue_tests() {
    f.reset(); f.access(1); start(); ia::create(sw, attrs(1)); auto before = ia::status();
    auto p = arp(target("192.0.2.1"));
    { std::lock_guard<std::mutex> l(f.sent_mutex); f.hold_send = true; }
    inject(p, 201, before.traps[0]);
    {
        std::unique_lock<std::mutex> l(f.sent_mutex);
        assert(f.sent_cv.wait_for(l, std::chrono::seconds(3), [] { return f.entered_send; }));
    }
    // Worker is inside SAI while callback is still bounded and does not call SDK.
    for (unsigned i = 0; i < 1000; ++i) inject(p, 201, before.traps[0]);
    { std::lock_guard<std::mutex> l(f.sent_mutex); f.hold_send = false; } f.sent_cv.notify_all();
    auto after = ia::status(); assert(after.admitted - before.admitted <= 65 && after.dropped - before.dropped >= 936);
    wait_stat([&](const ia::Status& s) { return s.queued == 0; });
    // Admission remains bounded to 100 in this fixed one-second window, independent of queue drain.
    for (unsigned i = 0; i < 1000; ++i) inject(p, 201, before.traps[0]);
    after = ia::status(); assert(after.admitted - before.admitted <= 100);
    ia::stop(); auto sent = f.sent.size();
    for (unsigned i = 0; i < 1000; ++i) inject(p, 201, before.traps[0]);
    assert(f.sent.size() == sent && ia::status().queued == 0);
    // Concurrent SDK callback producers may outlive stop, but cannot access
    // removed SDK objects or send after worker join. No callback retains a buffer.
    f.reset(); f.access(1); start(); ia::create(sw, attrs(1)); before = ia::status();
    std::atomic<bool> go{false};
    auto flood = [&] {
        while (!go.load()) std::this_thread::yield();
        for (unsigned i = 0; i < 10000; ++i) inject(p, 201, before.traps[0]);
    };
    std::thread first(flood), second(flood); go = true;
    ia::stop(); sent = f.sent.size(); first.join(); second.join();
    assert(f.sent.size() == sent && f.owned() == 0 && ia::status().queued == 0);
}
} // namespace
int main() {
    packet_tests(); setup_tests(); address_tests(); worker_tests(); bounded_queue_tests(); ia::stop();
    std::cout << "interface_address: pure packet + fake SAI lifecycle/ownership/topology/worker/bounds tests passed\n";
    return 0;
}
