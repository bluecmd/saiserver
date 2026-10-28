// The legacy SAI RPC handler without a listener, so tests can drive it
// through a processor against a fake SDK.
#pragma once
#include "switch_sai_rpc.h"
#include <memory>

std::shared_ptr<switch_sai::switch_sai_rpcIf> make_switch_sai_rpc_handler();
