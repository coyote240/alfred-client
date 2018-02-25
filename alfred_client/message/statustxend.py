from .message import Message, MessageTypeId


@MessageTypeId(3)
class StatusTxEnd(Message):

    message_length = 4
    packet_body = {
        'transaction_id': 0,
        'number_of_packets': 0
    }

    def __init__(self, container=None):
        super().__init__(container)

    @property
    def length(self):
        return self.message_length

    @property
    def transaction_id(self):
        return self.packet_body.get('transaction_id')

    @transaction_id.setter
    def transaction_id(self, value):
        self.packet_body['transaction_id'] = value

    @property
    def number_of_packets(self):
        return self.packet_body.get('number_of_packets')

    @number_of_packets.setter
    def number_of_packets(self, value):
        self.packet_body['number_of_packets'] = value

    def compose(self):
        return {
            'alfred_tlv': self.tlv,
            'packet_body': {
                'transaction_id': self.transaction_id,
                'number_of_packets': self.number_of_packets
            }
        }
