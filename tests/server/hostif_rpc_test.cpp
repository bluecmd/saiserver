// Drive the legacy hostif RPCs through the real handler and Thrift processor
// against the fake SDK. Each case checks the sai_attribute_t that reaches the
// SDK, not just the RPC status. No sockets or SDK DSO.
#include "tests/server/fake_sdk.h"
#include "src/bounded_rpc_processor.h"
#include "src/switch_sai_rpc_handler.h"
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/transport/TBufferTransports.h>
#include <atomic>
#include <cassert>
#include <cstring>
#include <functional>
#include <iostream>
#include <string>
#include <vector>

using namespace fake_sdk;

sai_object_id_t gSwitchId = sw;
extern "C" sai_status_t sai_api_query(sai_api_t api, void** out) { return query(api, out); }
extern "C" sai_status_t sai_api_uninitialize() { return SAI_STATUS_SUCCESS; }

namespace {
const sai_object_id_t hif = 7000, port = 201;
struct Call { sai_object_id_t id; std::vector<sai_attribute_t> attrs; };
std::vector<Call> sets, creates;
sai_status_t set_status = SAI_STATUS_SUCCESS;

sai_status_t set_hostif(sai_object_id_t id, const sai_attribute_t* attr) {
    sets.push_back({id, {*attr}}); return set_status;
}
sai_status_t create_hostif(sai_object_id_t* id, sai_object_id_t s, uint32_t n, const sai_attribute_t* attrs) {
    assert(s == sw);
    creates.push_back({s, std::vector<sai_attribute_t>(attrs, attrs + n)}); *id = hif; return SAI_STATUS_SUCCESS;
}

switch_sai::sai_thrift_attribute_t attribute(sai_attr_id_t id) {
    switch_sai::sai_thrift_attribute_t a; a.id = id; return a;
}

struct Rpc {
    std::shared_ptr<apache::thrift::transport::TMemoryBuffer> req =
        std::make_shared<apache::thrift::transport::TMemoryBuffer>(),
        res = std::make_shared<apache::thrift::transport::TMemoryBuffer>();
    std::shared_ptr<apache::thrift::protocol::TBinaryProtocol> in =
        std::make_shared<apache::thrift::protocol::TBinaryProtocol>(req),
        out = std::make_shared<apache::thrift::protocol::TBinaryProtocol>(res);
    std::atomic<bool> accepting{true};
    BoundedRpcProcessor processor{make_switch_sai_rpc_handler(), accepting};
    switch_sai::switch_sai_rpcClient client{out, in};

    switch_sai::sai_thrift_status_t set(const switch_sai::sai_thrift_attribute_t& a) {
        sets.clear(); client.send_sai_thrift_set_hostif_attribute(hif, a);
        assert(processor.process(in, out, nullptr));
        const auto status = client.recv_sai_thrift_set_hostif_attribute();
        assert(sets.size() == 1 && sets[0].id == hif && sets[0].attrs[0].id == sai_attr_id_t(a.id));
        return status;
    }
};

void set_cases(Rpc& rpc) {
    // The regression: OPER_STATUS was parsed as a trap-group attribute, fell
    // through the default branch and reached the SDK as false.
    auto up = attribute(SAI_HOSTIF_ATTR_OPER_STATUS); up.value.booldata = true;
    assert(rpc.set(up) == SAI_STATUS_SUCCESS && sets[0].attrs[0].value.booldata);
    auto down = attribute(SAI_HOSTIF_ATTR_OPER_STATUS); down.value.booldata = false;
    assert(rpc.set(down) == SAI_STATUS_SUCCESS && !sets[0].attrs[0].value.booldata);

    auto queue = attribute(SAI_HOSTIF_ATTR_QUEUE); queue.value.u32 = 7;
    assert(rpc.set(queue) == SAI_STATUS_SUCCESS && sets[0].attrs[0].value.u32 == 7);

    auto tag = attribute(SAI_HOSTIF_ATTR_VLAN_TAG); tag.value.s32 = SAI_HOSTIF_VLAN_TAG_KEEP;
    assert(rpc.set(tag) == SAI_STATUS_SUCCESS && sets[0].attrs[0].value.s32 == SAI_HOSTIF_VLAN_TAG_KEEP);

    // The SDK's own answer is returned, not a blanket SUCCESS.
    set_status = SAI_STATUS_NOT_SUPPORTED;
    assert(rpc.set(up) == SAI_STATUS_NOT_SUPPORTED && sets[0].attrs[0].value.booldata);
    set_status = SAI_STATUS_SUCCESS;
}

// The Thrift error the client gets for a request the handler rejects.
std::string rejection(const std::function<void()>& call) {
    try { call(); } catch (const apache::thrift::TApplicationException& e) { return e.what(); }
    assert(!"expected the RPC to be rejected"); return "";
}

void rejection_cases(Rpc& rpc) {
    // An attribute the handler cannot translate used to reach the SDK zeroed,
    // with a SUCCESS reply. It must be rejected before any SDK call.
    sets.clear(); creates.clear();
    auto mcgrp = attribute(SAI_HOSTIF_ATTR_GENETLINK_MCGRP_NAME); mcgrp.value.chardata = "group";
    auto message = rejection([&] {
        rpc.client.send_sai_thrift_set_hostif_attribute(hif, mcgrp);
        assert(rpc.processor.process(rpc.in, rpc.out, nullptr));
        rpc.client.recv_sai_thrift_set_hostif_attribute();
    });
    assert(message.find("unsupported hostif attribute id") != std::string::npos && sets.empty());

    auto type = attribute(SAI_HOSTIF_ATTR_TYPE); type.value.s32 = SAI_HOSTIF_TYPE_NETDEV;
    rejection([&] {
        rpc.client.send_sai_thrift_create_hostif({type, mcgrp});
        assert(rpc.processor.process(rpc.in, rpc.out, nullptr));
        rpc.client.recv_sai_thrift_create_hostif();
    });
    assert(creates.empty());

    // NAME is a C string in a fixed buffer: an unpadded name is copied exactly
    // (it used to be over-read), one that cannot fit is rejected.
    auto obj = attribute(SAI_HOSTIF_ATTR_OBJ_ID); obj.value.oid = port;
    auto name = attribute(SAI_HOSTIF_ATTR_NAME); name.value.chardata = "Ethernet0";
    rpc.client.send_sai_thrift_create_hostif({type, obj, name});
    assert(rpc.processor.process(rpc.in, rpc.out, nullptr));
    assert(rpc.client.recv_sai_thrift_create_hostif() == static_cast<int64_t>(hif));
    assert(creates.size() == 1 && std::string(creates[0].attrs[2].value.chardata) == "Ethernet0");
    name.value.chardata = std::string(SAI_HOSTIF_NAME_SIZE, 'x');
    message = rejection([&] {
        rpc.client.send_sai_thrift_create_hostif({type, obj, name});
        assert(rpc.processor.process(rpc.in, rpc.out, nullptr));
        rpc.client.recv_sai_thrift_create_hostif();
    });
    assert(message.find("hostif name longer than") != std::string::npos && creates.size() == 1);
    creates.clear();
}

void create_case(Rpc& rpc) {
    std::vector<switch_sai::sai_thrift_attribute_t> list;
    auto type = attribute(SAI_HOSTIF_ATTR_TYPE); type.value.s32 = SAI_HOSTIF_TYPE_NETDEV; list.push_back(type);
    auto obj = attribute(SAI_HOSTIF_ATTR_OBJ_ID); obj.value.oid = port; list.push_back(obj);
    auto name = attribute(SAI_HOSTIF_ATTR_NAME);
    name.value.chardata = std::string("Ethernet0").append(SAI_HOSTIF_NAME_SIZE, '\0'); list.push_back(name);
    auto up = attribute(SAI_HOSTIF_ATTR_OPER_STATUS); up.value.booldata = true; list.push_back(up);
    auto queue = attribute(SAI_HOSTIF_ATTR_QUEUE); queue.value.u32 = 3; list.push_back(queue);
    auto tag = attribute(SAI_HOSTIF_ATTR_VLAN_TAG); tag.value.s32 = SAI_HOSTIF_VLAN_TAG_ORIGINAL; list.push_back(tag);

    rpc.client.send_sai_thrift_create_hostif(list);
    assert(rpc.processor.process(rpc.in, rpc.out, nullptr));
    assert(rpc.client.recv_sai_thrift_create_hostif() == static_cast<int64_t>(hif));
    assert(creates.size() == 1 && creates[0].attrs.size() == list.size());
    const auto& a = creates[0].attrs;
    for (size_t i = 0; i < list.size(); ++i) assert(a[i].id == sai_attr_id_t(list[i].id));
    assert(a[0].value.s32 == SAI_HOSTIF_TYPE_NETDEV && a[1].value.oid == port);
    assert(std::strcmp(a[2].value.chardata, "Ethernet0") == 0);
    assert(a[3].value.booldata && a[4].value.u32 == 3 && a[5].value.s32 == SAI_HOSTIF_VLAN_TAG_ORIGINAL);
}
}

int main() {
    f.reset();
    f.hostif.set_hostif_attribute = set_hostif;
    f.hostif.create_hostif = create_hostif;
    Rpc rpc;
    set_cases(rpc);
    rejection_cases(rpc);
    create_case(rpc);
    std::cout << "hostif RPC: OPER_STATUS/QUEUE/VLAN_TAG reach set_hostif_attribute and create_hostif\n";
}
