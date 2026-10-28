// Bounded management extension; see docs/tui-api.md.
namespace cpp sai_tui
namespace py sai_tui

exception RpcError {
    1: i32 status;
    2: string message;
}
struct Object {
    1: string kind;
    2: string key;
    3: map<string,string> attributes;
}
struct Inventory {
    1: list<Object> objects;
    2: list<string> warnings;
}
service SaiTui {
    Inventory tui_snapshot() throws (1: RpcError error);
    Object tui_get(1: string kind, 2: string key) throws (1: RpcError error);
    Object tui_create(1: string kind, 2: map<string,string> attributes) throws (1: RpcError error);
    Object tui_set(1: string kind, 2: string key, 3: map<string,string> attributes) throws (1: RpcError error);
    void tui_remove(1: string kind, 2: string key) throws (1: RpcError error);
    map<string,i64> tui_port_counters(1: string key) throws (1: RpcError error);
}
