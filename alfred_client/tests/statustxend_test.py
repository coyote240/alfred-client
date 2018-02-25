import unittest
from alfred_client.message import StatusTxEnd
from alfred_client.packet.struct import alfred_packet


expected_bytes = b'\x03\x00\x00\x04\x00\x00\x00\x00'


class TestCreateStatusTxEnd(unittest.TestCase):

    def setUp(self):
        self.message = StatusTxEnd()

    def test_message_type(self):
        self.assertEqual(self.message.type, 3)

    def test_transaction_id(self):
        self.assertEqual(self.message.transaction_id, 0)

    def test_number_of_packets(self):
        self.assertEqual(self.message.number_of_packets, 0)

    def test_bytes(self):
        self.assertEqual(bytes(self.message), expected_bytes)


class TestParseStatusTxEnd(unittest.TestCase):

    def setUp(self):
        self.container = alfred_packet.parse(expected_bytes)
        self.message = StatusTxEnd(self.container)

    def test_message_type(self):
        self.assertEqual(self.message.type, 3)

    def test_message_version(self):
        self.assertEqual(self.message.version, 0)

    def test_message_length(self):
        self.assertEqual(self.message.length, 4)

    def test_transaction_id(self):
        self.assertEqual(self.message.transaction_id, 0)

    def test_number_of_packets(self):
        self.assertEqual(self.message.number_of_packets, 0)
