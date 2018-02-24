from .message import Message, MessageTypeId


@MessageTypeId(0)
class PushData(Message):

    def __init__(self, container=None):
        self.source_mac_address = None
        self._data = []
        super().__init__(container)

    @property
    def length(self):
        if self._length > 0:
            return self._length
        return 4 + sum([10 + b['length'] for b in self._data])

    def add_data_block(self, typeid, version, data):
        enc_data = bytes(data, 'utf-8')
        len_data = len(enc_data)

        block = {
            'source_mac_address': self.source_mac_address,  # size 6
            'type': typeid,                                 # size 1
            'version': version,                             # size 1
            'length': len_data,                             # size 2
            'data': enc_data
        }
        self._data.append(block)

    def compose(self):
        return {
            'alfred_tlv': self.tlv,
            'packet_body': {
                'transaction_id': 0,
                'sequence_number': 0,
                'alfred_data': self._data
            }
        }
