// Single ingress gate: do not allow any legacy entrypoint to bypass the
// responder's shared SAI lock. The whitelist includes reads as well as writes.
#pragma once
#include "switch_sai_rpc.h"
#include "tui_rpc.h"
#include <atomic>
#include <thrift/TApplicationException.h>

class BoundedRpcProcessor : public switch_sai::switch_sai_rpcProcessor {
public:
    BoundedRpcProcessor(const std::shared_ptr<switch_sai::switch_sai_rpcIf>& handler,
                        std::atomic<bool>& accepting)
        : switch_sai::switch_sai_rpcProcessor(handler), accepting_(accepting) {}
protected:
    bool dispatchCall(apache::thrift::protocol::TProtocol* in,
                      apache::thrift::protocol::TProtocol* out,
                      const std::string& name, int32_t seqid, void* context) override {
        const bool bounded_call = name == "tui_snapshot" || name == "tui_get" ||
            name == "tui_create" || name == "tui_set" || name == "tui_remove" ||
            name == "tui_port_counters";
        if (!accepting_.load() || (tui_rpc::bounded_only() && !bounded_call)) {
            using namespace apache::thrift;
            using namespace apache::thrift::protocol;
            in->skip(T_STRUCT); in->readMessageEnd(); in->getTransport()->readEnd();
            TApplicationException e(TApplicationException::UNKNOWN_METHOD,
                "RPC rejected: server stopping or interface_address bounded-only mode; use tui_* API");
            out->writeMessageBegin(name, T_EXCEPTION, seqid); e.write(out);
            out->writeMessageEnd(); out->getTransport()->writeEnd(); out->getTransport()->flush();
            return true;
        }
        return switch_sai::switch_sai_rpcProcessor::dispatchCall(in, out, name, seqid, context);
    }
private:
    std::atomic<bool>& accepting_;
};
