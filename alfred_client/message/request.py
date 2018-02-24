from .message import Message, MessageTypeId


@MessageTypeId(2)
class Request(Message):
    pass
