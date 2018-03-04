from construct import (
    Array, Byte, Bytes,
    Struct, Switch, Int8ub, Int16ub
)
from .adapters import MACAdapter

alfred_tlv = Struct(
    'type' / Int8ub,
    'version' / Int8ub,
    'length' / Int16ub
)

alfred_announce_master = Struct()

alfred_request = Struct(
    'requested_type' / Int8ub,
    'transaction_id' / Int16ub
)

alfred_status_end = Struct(
    'transaction_id' / Int16ub,
    'number_of_packets' / Int16ub
)

alfred_status_error = Struct(
    'transaction_id' / Int16ub,
    'error_code' / Int16ub
)

alfred_mode_switch = Struct(
    'mode' / Int8ub
)

alfred_data_block = Struct(
    'source_mac_address' / MACAdapter(Byte[6]),
    'type' / Int8ub,
    'version' / Int8ub,
    'length' / Int16ub,
    'data' / Bytes(lambda ctx: ctx.length)
)

alfred_transaction_mgmt = Struct(
    'transaction_id' / Int16ub,
    'sequence_number' / Int16ub,
)

alfred_push_data = Struct(
    'transaction_id' / Int16ub,
    'sequence_number' / Int16ub,
    'alfred_data' / Array(1, alfred_data_block)
)

alfred_packet = Struct(
    'alfred_tlv' / alfred_tlv,
    'packet_body' / Switch(lambda ctx: ctx.alfred_tlv.type, {
        0: alfred_push_data,
        1: alfred_announce_master,
        2: alfred_request,
        3: alfred_status_end,
        4: alfred_status_error,
        5: alfred_mode_switch
    })
)
