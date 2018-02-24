from .message import Message, MessageTypeId


@MessageTypeId(1)
class AnnounceMaster(Message):
    pass
