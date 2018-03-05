import socket
import tornado.web
from tornado import gen
from tornado.options import options
from alfred_client.packet import struct
from alfred_client.message import Request


class VisHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def get(self):
        txid = 1

        request = Request()
        request.requested_type = 1
        request.transaction_id = txid

        response = yield self.send(bytes(request))
        print(response)

        data = [{
            'source_mac_address': record.source_mac_address,
            'vis': record.data.decode('utf')
        } for record in response]

        self.write({
            'nodes': data
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
                retval.append(data_block.alfred_data[0])

        raise gen.Return(retval)
