// Notification view regression tests. No switch or vendor library required.
#include "src/notifications.h"
#include <cassert>

std::vector<std::pair<sai_fdb_entry_t, sai_object_id_t>> gFdbMap;

int main() {
    sai_attribute_t attrs[2] = {};
    sai_fdb_event_notification_data_t events[2] = {};
    for (int i = 0; i < 2; ++i) {
        attrs[i].id = SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID;
        attrs[i].value.oid = 100 + i;
        events[i].event_type = SAI_FDB_EVENT_LEARNED;
        events[i].fdb_entry.switch_id = 1;
        events[i].fdb_entry.bv_id = 10;
        events[i].fdb_entry.mac_address[5] = i + 1;
        events[i].attr_count = 1;
        events[i].attr = &attrs[i];
    }
    on_fdb_event(2, events);
    assert(gFdbMap.size() == 2);
    assert(gFdbMap[0].second == 100 && gFdbMap[1].second == 101);
    on_fdb_event(2, events); // repeated learning must not duplicate entries
    assert(gFdbMap.size() == 2);
    events[0].event_type = SAI_FDB_EVENT_MOVE;
    attrs[0].value.oid = 102;
    on_fdb_event(1, events);
    assert(gFdbMap[0].second == 102);
    events[0].event_type = SAI_FDB_EVENT_AGED;
    on_fdb_event(1, events);
    assert(gFdbMap.size() == 1 && gFdbMap[0].second == 101);
    events[0].event_type = SAI_FDB_EVENT_FLUSHED;
    attrs[0].value.oid = 999;
    on_fdb_event(1, events); // other port must survive
    assert(gFdbMap.size() == 1);
    events[0].attr_count = 0; // omitted port means all ports within this VLAN
    on_fdb_event(1, events);
    assert(gFdbMap.empty());
    events[0].event_type = SAI_FDB_EVENT_LEARNED;
    events[0].attr_count = 1;
    on_fdb_event(2, events);
    assert(gFdbMap.size() == 2);
    events[0].event_type = SAI_FDB_EVENT_FLUSHED;
    events[0].fdb_entry.bv_id = SAI_NULL_OBJECT_ID;
    events[0].attr_count = 0;
    on_fdb_event(1, events);
    assert(gFdbMap.empty());
    on_fdb_event(0, nullptr);
}
