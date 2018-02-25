import unittest
from alfred_client.message import AnnounceMaster
from alfred_client.packet.struct import alfred_packet


expected_bytes = b'\x01\x00\x00\x00'


class TestCreateAnnounceMaster(unittest.TestCase):

    def setUp(self):
        self.message = AnnounceMaster()

    def test_message_type(self):
        self.assertEqual(self.message.type, 1)

    def test_length(self):
        self.assertEqual(self.message.length, 0)

    def test_bytes(self):
        self.assertEqual(bytes(self.message), expected_bytes)


class TestParseAnnounceMaster(unittest.TestCase):

    def setUp(self):
        self.container = alfred_packet.parse(expected_bytes)
        self.message = AnnounceMaster(self.container)

    def test_message_type(self):
        self.assertEqual(self.message.type, 1)

    def test_message_version(self):
        self.assertEqual(self.message.version, 0)

    def test_message_length(self):
        self.assertEqual(self.message.length, 0)
