import unittest
from alfred_client.message import StatusError
from alfred_client.packet.struct import alfred_packet


expected_bytes = b'\x04\x00\x00\x04\x00\x00\x00\x00'


class TestCreateStatusErrorEnd(unittest.TestCase):

    def setUp(self):
        self.message = StatusError()

    def test_message_type(self):
        self.assertEqual(self.message.type, 4)

    def test_transaction_id(self):
        self.assertEqual(self.message.transaction_id, 0)

    def test_error_code(self):
        self.assertEqual(self.message.error_code, 0)

    def test_bytes(self):
        self.assertEqual(bytes(self.message), expected_bytes)


class TestParseStatusErrorEnd(unittest.TestCase):

    def setUp(self):
        self.container = alfred_packet.parse(expected_bytes)
        self.message = StatusError(self.container)

    def test_message_type(self):
        self.assertEqual(self.message.type, 4)

    def test_message_version(self):
        self.assertEqual(self.message.version, 0)

    def test_message_length(self):
        self.assertEqual(self.message.length, 4)

    def test_transaction_id(self):
        self.assertEqual(self.message.transaction_id, 0)

    def test_error_code(self):
        self.assertEqual(self.message.error_code, 0)
