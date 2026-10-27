extern "C" {
int start_sai_thrift_rpc_server(int port);
void stop_sai_thrift_rpc_server();
bool sai_thrift_rpc_server_running();
}
