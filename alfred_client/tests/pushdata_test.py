import unittest
from alfred_client.message import PushData
from alfred_client.packet.struct import alfred_packet


expected_mac = '5e:5c:ce:ca:93:58'
expected_message = 'raspberrypi\n'
expected_length = len(expected_message)
expected_bytes = b'\x00\x00\x00\x1a\x00\x00\x00\x00^\\\xce\xca\x93Xc\x00\x00\x0craspberrypi\n' # noqa


class TestCreatePushData(unittest.TestCase):

    def setUp(self):
        self.message = PushData()
        self.message.source_mac_address = expected_mac

    def test_message_type(self):
        self.assertEqual(self.message.type, 0)

    def test_source_mac_address(self):
        self.assertEqual(self.message.source_mac_address, expected_mac)

    def test_add_data_block(self):
        self.message.add_data_block(99, 0, expected_message)
        self.assertIn('length', self.message._data[0])

    def test_calculates_correct_data_value_length(self):
        self.message.add_data_block(99, 0, expected_message)
        self.assertEqual(self.message._data[0]['length'], expected_length)

    def test_calculates_correct_message_length(self):
        self.message.add_data_block(99, 0, expected_message)
        self.assertEqual(self.message.length, 26)

    def test_bytes(self):
        self.message.add_data_block(99, 0, expected_message)
        self.assertEqual(bytes(self.message), expected_bytes)


class TestParsePushData(unittest.TestCase):

    def setUp(self):
        self.container = alfred_packet.parse(expected_bytes)
        self.message = PushData(self.container)

    def test_message_type(self):
        self.assertEqual(self.message.type, 0)

    def test_message_version(self):
        self.assertEqual(self.message.version, 0)

    def test_message_length(self):
        self.assertEqual(self.message.length, 26)
