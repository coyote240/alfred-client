import unittest
from alfred_client.message import MetaMessage, Message, MessageTypeId


expected_bytes = b'\x00\x00\x00\x17\x00\x00\x00\x00r\x00\x01\x93\x9c`\x00\x00\x00\x03foo' # noqa


@MessageTypeId(99)
class MockMessage(Message):

    def __init__(self):
        super().__init__()


class TestMetaMessage(unittest.TestCase):

    def setUp(self):
        self.message = MockMessage()

    @unittest.skip('Need to dig into metaclass testing')
    def test_message_types(self):
        self.assertIn(MockMessage, MetaMessage.message_types)


class TestMessage(unittest.TestCase):

    def setUp(self):
        self.message = Message()

    def test_default_type(self):
        self.assertEqual(self.message.type, 0)

    def test_default_version(self):
        self.assertEqual(self.message.version, 0)

    def test_default_length(self):
        self.assertEqual(self.message.length, 0)

    def test_tlv(self):
        self.assertEqual(self.message.tlv, {
            'type': 0,
            'version': 0,
            'length': 0
        })

    def test_compose(self):
        comp = self.message.compose()
        self.assertEqual(comp, {
            'alfred_tlv': {
                'type': 0,
                'version': 0,
                'length': 0
            },
            'packet_body': {}
        })


class TestMessageTypeIdDecorator(unittest.TestCase):

    def setUp(self):
        self.message = MockMessage()

    def test_message_type(self):
        self.assertEqual(self.message.type, 99)
