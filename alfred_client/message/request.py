from .message import Message, MessageTypeId


@MessageTypeId(2)
class Request(Message):

    message_length = 3  # alfred_request_v0 has a fixed size
    packet_body = {
        'requested_type': 0,
        'transaction_id': 0
    }

    def __init__(self, container=None):
        super().__init__(container)

    @property
    def length(self):
        return self.message_length

    @property
    def requested_type(self):
        return self.packet_body.get('requested_type')

    @requested_type.setter
    def requested_type(self, value):
        self.packet_body['requested_type'] = value

    @property
    def transaction_id(self):
        return self.packet_body.get('transaction_id')

    @transaction_id.setter
    def transaction_id(self, value):
        self.packet_body['transaction_id'] = value

    def compose(self):
        return {
            'alfred_tlv': self.tlv,
            'packet_body': {
                'requested_type': self.requested_type,
                'transaction_id': self.transaction_id
            }
        }
