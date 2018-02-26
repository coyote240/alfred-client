import socket
import tornado.web
from tornado import gen
from tornado.options import options
from alfred_client.message import Request, Message


class DataHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def get(self, datatype=None):
        txid = 1

        request = Request()
        request.requested_type = int(datatype)
        request.transaction_id = txid

        data = yield self.send(bytes(request))
        message = Message.factory(data)
        self.write({
            'type': message.type,
            'length': message.length,
            'data': message.data
        })

    @gen.coroutine
    def send(self, packet):
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(options.socket_address)
            s.sendall(packet)
            data = s.recv(2048)

        raise gen.Return(data)
