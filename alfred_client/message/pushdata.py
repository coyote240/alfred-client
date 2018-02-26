from .message import Message, MessageTypeId


@MessageTypeId(0)
class PushData(Message):

    packet_body = {
        'transaction_id': 0,
        'sequence_number': 0,
        'alfred_data': []
    }

    def __init__(self, container=None):
        self.source_mac_address = None

        self._data = []
        super().__init__(container)

    @property
    def length(self):
        if self._length > 0:
            return self._length
        return 4 + sum([10 + b['length'] for b in self._data])

    @property
    def transaction_id(self):
        return self.packet_body.get('transaction_id')

    @transaction_id.setter
    def transaction_id(self, value):
        self.packet_body['transaction_id'] = value

    @property
    def sequence_number(self):
        return self.packet_body.get('sequence_number')

    @sequence_number.setter
    def sequence_number(self, value):
        self.packet_body['sequence_number'] = value

    @property
    def data(self):
        frame = bytearray()
        for block in self.packet_body.alfred_data:
            frame.extend(block.data)
        return frame.decode()

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
