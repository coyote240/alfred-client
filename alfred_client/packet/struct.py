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

'''
[Container
    (source_mac_address='7e:eb:58:b5:ec:ba')
    (type=1)
    (version=1)
    (length=38)
    (data=b"")]
'''

vis_test = b"\x00\x00\x00\x00\x00\x00\x01\x03\xb8'\xeb\xa3\n\x19\xb8'\xeb\n\xc0\x9b\x00\xff\xb8'\xeb\xac7\x1d\x00\xff~\xebX\xb5\xec\xba\xff\x00"  # noqa

vis_iface = Struct(
    'mac' / MACAdapter(Byte[6])
)

vis_entry = Struct(
    'mac' / MACAdapter(Byte[6]),
    'ifindex' / Int8ub,
    'qual' / Int8ub
)

vis_v1 = Struct(
    'mac' / MACAdapter(Byte[6]),
    'iface_n' / Int8ub,
    'entries_n' / Int8ub,
    'ifaces' / Array(lambda ctx: ctx.iface_n, vis_iface),
    'entries' / Array(lambda ctx: ctx.entries_n, vis_entry)
)

iface_list_entry = Struct(
    'name' / Bytes(256),
    'mac' / MACAdapter(Byte[6]),
    'devindex' / Int16ub
)
