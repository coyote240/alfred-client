from .message import Message, MessageTypeId


@MessageTypeId(1)
class AnnounceMaster(Message):

    message_length = 0

    def __init__(self, container=None):
        super().__init__(container)

    @property
    def length(self):
        return self.message_length

    def compose(self):
        return {
            'alfred_tlv': self.tlv,
            'packet_body': {}
        }
