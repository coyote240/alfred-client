from packet.struct import alfred_packet


class MetaMessage(type):

    message_types = []

    def __new__(mcs, name, bases, class_dict):
        cls = type.__new__(mcs, name, bases, class_dict)
        mcs.message_types.append(cls)
        return cls

    @classmethod
    def factory(mcs, packet):
        container = alfred_packet.parse(packet)
        typeid = container.alfred_tlv.type

        for message_type in mcs.message_types:
            if message_type._message_type == typeid:
                return message_type(container)

        return Message(container)


class MessageTypeId(object):

    def __init__(self, message_type):
        self._message_type = message_type

    def __call__(self, cls):
        cls._message_type = self._message_type
        return cls


class Message(dict):

    __metaclass__ = MetaMessage
    _message_type = 0
    _version = 0
    _length = 0

    def __init__(self, container=None):
        if container is not None:
            self.read(container)

    def read(self, container):
        self._message_type = container.alfred_tlv.type
        self._version = container.alfred_tlv.version
        self._length = container.alfred_tlv.length

        self.packet_body = container.packet_body

    @property
    def type(self):
        return self._message_type

    @property
    def version(self):
        return self._version

    @property
    def length(self):
        return self._length

    @property
    def tlv(self):
        return {
            'type': self._message_type,
            'version': self._version,
            'length': self._length
        }

    def _compose(self):
        return {
            'alfred_tlv': self.tlv,
            'packet_body': {}
        }

    def __bytes__(self):
        structure = self._compose()
        return alfred_packet.build(structure)


@MessageTypeId(0)
class PushData(Message):

    def __init__(self, container=None):
        self.source_mac_address = None
        self._data = []
        super().__init__(container)

    def add_data_block(self, typeid, version, data):
        block = {
            'source_mac_address': self.source_mac_address,
            'type': self.type,
            'version': self.version,
            'length': len(data),
            'data': bytes(data, 'utf-8')}
        self._data.append(block)

    def _compose(self):
        return {
            'alfred_tlv': self.tlv,
            'packet_body': {
                'transaction_id': 0,
                'sequence_number': 0,
                'alfred_data': self._data
            }
        }


@MessageTypeId(1)
class AnnounceMaster(Message):
    pass


@MessageTypeId(2)
class Request(Message):
    pass


@MessageTypeId(3)
class StatusTxEnd(Message):
    pass


@MessageTypeId(4)
class StatusError(Message):
    pass


@MessageTypeId(5)
class ModeSwitch(Message):
    pass
