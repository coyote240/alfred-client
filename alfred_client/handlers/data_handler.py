import uuid
import socket
import tornado.web
from tornado import gen
from tornado.options import options
from alfred_client.message import Request


class DataHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def get(self, datatype=None):
        txid = uuid.uuid4().hex

        request = Request()
        request.requested_type = datatype
        request.transaction_id = txid

        data = yield self.send(bytes(request))
        self.write(data)

    @gen.coroutine
    def send(self, packet):
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(options.socket_address)
            s.sendall(packet)
            data = s.recv(2048)

        raise gen.Return(data)
