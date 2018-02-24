from .message import Message, MessageTypeId


@MessageTypeId(3)
class StatusTxEnd(Message):
    pass
