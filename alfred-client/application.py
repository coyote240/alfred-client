import signal
import socket
from netifaces import ifaddresses, AF_INET6, AF_LINK
import tornado.web
import tornado.ioloop
from packet.struct import alfred_packet

socket_address = '/var/run/alfred.sock'
bat_addr = ifaddresses('bat0')[AF_INET6][0]['addr']
bat_mac = ifaddresses('bat0')[AF_LINK][0]['addr']
message = str.encode(bat_addr)

'''
Container:
    alfred_tlv = Container:
        type = 0
        version = 0
        length = 26
    packet_body = Container:
        transaction_id = 1
        sequence_number = 0
        alfred_data = ListContainer:
            Container:
                source_mac_address = 5e:5c:ce:ca:93:58 (total 17)
                type = 65
                version = 0
                length = 12
                data = raspberrypi\n (total 12)
'''

update = alfred_packet.build({
    'alfred_tlv': {
        'type': 0,
        'version': 0,
        'length': 44
    },
    'packet_body': {
        'transaction_id': 1,
        'sequence_number': 0,
        'alfred_data': [{
            'source_mac_address': bat_mac,
            'type': 66,
            'version': 0,
            'length': len(message),
            'data': message
        }]
    }
})

status = alfred_packet.build({
    'alfred_tlv': {
        'type': 3,
        'version': 0,
        'length': 4
    },
    'packet_body': {
        'transaction_id': 1,
        'number_of_packets': 1
    }
})


def read_alfred_socket():
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(socket_address)
        s.sendall(update)


class Application(tornado.web.Application):

    def __init__(self):
        self.init_signal_handlers()

    def init_handlers(self):
        pass

    def init_signal_handlers(self):
        signal.signal(signal.SIGINT, self.interrupt_handler)
        if hasattr(signal, 'SIGQUIT'):
            signal.signal(signal.SIGQUIT, self.interrupt_handler)

    def interrupt_handler(self, signum, frame):
        tornado.ioloop.IOLoop.instance().add_callback_from_signal(
                lambda: tornado.ioloop.IOLoop.instance().stop())

    def start(self):
        tornado.ioloop.PeriodicCallback(read_alfred_socket, 5000).start()
        tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    Application().start()
