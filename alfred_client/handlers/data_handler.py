import socket
import tornado.web
from tornado import gen
from tornado.options import options
from alfred_client.packet import struct
from alfred_client.message import Request


class DataHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def get(self, datatype=None):
        txid = 1

        request = Request()
        request.requested_type = int(datatype)
        request.transaction_id = txid

        data = yield self.send(bytes(request))
        self.write({
            'data': data
        })

    @gen.coroutine
    def send(self, packet):
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(options.socket_address)
            s.sendall(packet)

            retval = []
            while True:
                # read header
                header = s.recv(struct.alfred_tlv.sizeof())
                if len(header) == 0:
                    break

                # read body
                tlv = struct.alfred_tlv.parse(header)
                body = s.recv(tlv.length)
                data_block = struct.alfred_push_data.parse(body)
                retval.append(data_block.alfred_data)

        raise gen.Return(retval)
