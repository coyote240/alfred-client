import socket
import tornado.web
from tornado import gen
from tornado.options import options
from alfred_client.message import PushData


class LEDHandler(tornado.web.RequestHandler):

    def initialize(self, bat_mac=None):
        self.bat_mac = bat_mac

    @gen.coroutine
    def post(self):
        value = self.get_argument('value')

        request = PushData()
        request.source_mac_address = self.bat_mac
        request.add_data_block(67, 0, value)

        self.send(bytes(request))

    @gen.coroutine
    def send(self, packet):
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(options.socket_address)
            s.sendall(packet)
