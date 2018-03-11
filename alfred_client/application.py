import json
import signal
import socket
from netifaces import ifaddresses, AF_INET, AF_INET6, AF_LINK
import tornado.web
import tornado.ioloop
from tornado.iostream import IOStream
from tornado.web import URLSpec
from tornado.httpserver import HTTPServer
from tornado.options import define, options
from alfred_client.message import Request, PushData
from alfred_client.packet import struct
from alfred_client import handlers

import RPi.GPIO as GPIO

define('socket_address', type=str, default='/var/run/alfred.sock',
       help='Path to the alfred socket')
define('web_port', type=int, default=8888,
       help='The port on which this application\'s web interface will listen.')
define('broadcast_port', type=int, default=44044,
       help='The port on which app will broadcast UDP host discovery packets')
define('bat_interface', type=str, default='bat0',
       help='The interface on which alfred listens')
define('web_interface', type=str, default='eth0',
       help='The interface to which the web application will bind')
define('ledpin', type=int, default=11,
       help='Pin used by demo')

define('config', help='Path to config file',
       callback=lambda path: options.parse_config_file(path, final=False))


class Application(tornado.web.Application):

    def __init__(self):
        self.init_handlers()
        self.init_signal_handlers()
        settings = self.init_settings()
        self.init_interfaces()
        self.init_gpio()

        super().__init__(self.handlers, **settings)

    def init_handlers(self):
        self.handlers = [
            URLSpec(r'/',
                    handlers.IndexHandler,
                    name='Index'),
            URLSpec(r'/data/(\d*)',
                    handlers.DataHandler,
                    name='Data'),
            URLSpec(r'/nodeinfo',
                    handlers.NodeInfoHandler,
                    name='NodeInfo'),
            URLSpec(r'/vis',
                    handlers.VisHandler,
                    name='Vis')]

    def init_settings(self):
        settings = {
            'socket_address': options.socket_address,
            'bat_interface': options.bat_interface,
            'web_interface': options.web_interface,
            'port': options.web_port}

        return settings

    def init_interfaces(self):
        bat_iface = ifaddresses(options.bat_interface)
        self.bat_addr = bat_iface[AF_INET6][0]['addr']
        self.bat_mac = bat_iface[AF_LINK][0]['addr']

        web_iface = ifaddresses(options.web_interface)
        self.web_addr = web_iface[AF_INET][0]['addr']
        self.web_broadcast_addr = web_iface[AF_INET][0]['broadcast']

    def init_signal_handlers(self):
        signal.signal(signal.SIGINT, self.interrupt_handler)
        if hasattr(signal, 'SIGQUIT'):
            signal.signal(signal.SIGQUIT, self.interrupt_handler)

    def interrupt_handler(self, signum, frame):
        GPIO.cleanup()
        tornado.ioloop.IOLoop.instance().add_callback_from_signal(
                lambda: tornado.ioloop.IOLoop.instance().stop())

    def init_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(options.ledpin, GPIO.OUT)

    def host_info_task(self):
        host_info = PushData()
        host_info.source_mac_address = self.bat_mac
        host_info.add_data_block(66, 0, self.bat_addr)

        if options.socket_address is None:
            return

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(options.socket_address)
            s.sendall(bytes(host_info))

    def alfred_task_reader(self):
        request = Request()
        request.requested_type = 67
        request.transaction_id = 1

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(options.socket_address)
            s.sendall(bytes(request))

            retval = []
            while True:
                header = s.recv(struct.alfred_tlv.sizeof())
                if len(header) == 0:
                    break

                tlv = struct.alfred_tlv.parse(header)
                body = s.recv(tlv.length)
                data_block = struct.alfred_push_data.parse(body)
                retval.append(data_block.alfred_data[0])

        # retval should be interpreted and put on a queue, but we'll hack it
        # for now
        for r in retval:
            val = r.data.decode()
            if val == 'on':
                GPIO.output(options.ledpin, GPIO.HIGH)
            else:
                GPIO.output(options.ledpin, GPIO.LOW)

    def discovery_address(self):
        message = json.dumps({
            'web_addr': self.web_addr,
            'web_port': options.web_port
        })
        self.discovery_stream.write(bytes(message, 'utf-8'))

    def start(self):
        server = HTTPServer(self)
        server.listen(options.web_port, address=self.web_addr)

        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.discovery_stream = IOStream(udp_sock)
        self.discovery_stream.connect((self.web_broadcast_addr,
                                       options.broadcast_port))

        # This should really point to a task queue
        tornado.ioloop.PeriodicCallback(self.discovery_address, 5000).start()
        tornado.ioloop.PeriodicCallback(self.host_info_task, 5000).start()
        tornado.ioloop.PeriodicCallback(self.alfred_task_reader, 500).start()

        tornado.ioloop.IOLoop.current().start()


def main():
    options.parse_command_line()
    Application().start()
