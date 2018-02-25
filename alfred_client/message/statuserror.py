from .message import Message, MessageTypeId


@MessageTypeId(4)
class StatusError(Message):

    message_length = 4
    packet_body = {
        'transaction_id': 0,
        'error_code': 0
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
    def error_code(self):
        return self.packet_body.get('error_code')

    @error_code.setter
    def error_code(self, value):
        self.packet_body['error_code'] = value

    def compose(self):
        return {
            'alfred_tlv': self.tlv,
            'packet_body': {
                'transaction_id': self.transaction_id,
                'error_code': self.error_code
            }
        }
