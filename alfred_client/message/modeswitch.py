from .message import Message, MessageTypeId


@MessageTypeId(5)
class ModeSwitch(Message):
    pass
