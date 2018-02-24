from .message import Message, MessageTypeId


@MessageTypeId(4)
class StatusError(Message):
    pass
