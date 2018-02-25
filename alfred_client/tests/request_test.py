import unittest
from alfred_client.message import Request
from alfred_client.packet.struct import alfred_packet


expected_bytes = b'\x02\x00\x00\x03c\x00\x00'


class TestCreateRequest(unittest.TestCase):

    def setUp(self):
        self.message = Request()
        self.message.requested_type = 99
        self.message.transaction_id = 0

    def test_message_type(self):
        self.assertEqual(self.message.type, 2)

    def test_bytes(self):
        self.assertEqual(bytes(self.message), expected_bytes)


class TestParseRequest(unittest.TestCase):

    def setUp(self):
        self.container = alfred_packet.parse(expected_bytes)
        self.message = Request(self.container)

    def test_message_type(self):
        self.assertEqual(self.message.type, 2)

    def test_message_version(self):
        self.assertEqual(self.message.version, 0)

    def test_message_length(self):
        self.assertEqual(self.message.length, 3)

    def test_requested_type(self):
        self.assertEqual(self.message.requested_type, 99)
