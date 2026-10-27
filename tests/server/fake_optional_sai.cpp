// Extends the baseline fake without changing its required-entrypoint behavior.
#include "../fake_sai.cpp"
extern "C" sai_status_t sai_get_object_key(sai_object_id_t sw, sai_object_type_t type,
                                           uint32_t* count, sai_object_key_t* keys) {
    if (sw == 42) throw 42;
    if (sw != UINT64_C(0xfedcba9876543210) || type != SAI_OBJECT_TYPE_HOSTIF_TRAP)
        return SAI_STATUS_INVALID_PARAMETER;
    const auto capacity = *count; *count = 1;
    if (capacity < 1) return SAI_STATUS_BUFFER_OVERFLOW;
    keys[0].key.object_id = UINT64_C(0xfedcba9876543211); return SAI_STATUS_SUCCESS;
}
extern "C" sai_object_type_t sai_object_type_query(sai_object_id_t id) {
    if (id == 42) throw 42;
    return id == UINT64_C(0xfedcba9876543211) ? SAI_OBJECT_TYPE_HOSTIF_TRAP : SAI_OBJECT_TYPE_NULL;
}
extern "C" sai_object_id_t sai_switch_id_query(sai_object_id_t id) {
    if (id == 42) throw 42;
    return id == UINT64_C(0xfedcba9876543211) ? UINT64_C(0xfedcba9876543210) : SAI_NULL_OBJECT_ID;
}
extern "C" sai_status_t sai_query_attribute_enum_values_capability(
    sai_object_id_t sw, sai_object_type_t type, sai_attr_id_t attr, sai_s32_list_t* values) {
    if (sw == 42) throw 42;
    if (sw != UINT64_C(0xfedcba9876543210) || type != SAI_OBJECT_TYPE_HOSTIF_PACKET ||
        attr != SAI_HOSTIF_PACKET_ATTR_HOSTIF_TX_TYPE) return SAI_STATUS_NOT_SUPPORTED;
    const auto capacity = values->count; values->count = 1;
    if (capacity < 1) return SAI_STATUS_BUFFER_OVERFLOW;
    values->list[0] = SAI_HOSTIF_TX_TYPE_PIPELINE_BYPASS; return SAI_STATUS_SUCCESS;
}
