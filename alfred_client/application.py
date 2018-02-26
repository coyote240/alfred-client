import signal
import socket
from netifaces import ifaddresses, AF_INET, AF_INET6, AF_LINK
import tornado.web
import tornado.ioloop
from tornado.web import URLSpec
from tornado.httpserver import HTTPServer
from tornado.options import define, options
from alfred_client.message import PushData
from alfred_client import handlers


define('socket_address', type=str, default='/var/run/alfred.sock',
       help='Path to the alfred socket')
define('port', type=int, default=8888,
       help='The port on which this applications web interface will listen.')
define('bat_interface', type=str, default='bat0',
       help='The interface on which alfred listens')
define('web_interface', type=str, default='eth0',
       help='The interface to which the web application will bind')
define('config', help='Path to config file',
       callback=lambda path: options.parse_config_file(path, final=False))


class Application(tornado.web.Application):

    def __init__(self):
        self.init_handlers()
        self.init_signal_handlers()
        settings = self.init_settings()
        self.init_interfaces()

        super().__init__(self.handlers, **settings)

    def init_handlers(self):
        self.handlers = [
            URLSpec(r'/data/(\d*)',
                    handlers.DataHandler,
                    name='Data')]

    def init_settings(self):
        settings = {
            'socket_address': options.socket_address,
            'bat_interface': options.bat_interface,
            'web_interface': options.web_interface,
            'port': options.port}

        return settings

    def init_interfaces(self):
        bat_iface = ifaddresses(options.bat_interface)
        self.bat_addr = bat_iface[AF_INET6][0]['addr']
        self.bat_mac = bat_iface[AF_LINK][0]['addr']

        web_iface = ifaddresses(options.web_interface)
        self.web_addr = web_iface[AF_INET][0]['addr']

    def init_signal_handlers(self):
        signal.signal(signal.SIGINT, self.interrupt_handler)
        if hasattr(signal, 'SIGQUIT'):
            signal.signal(signal.SIGQUIT, self.interrupt_handler)

    def interrupt_handler(self, signum, frame):
        tornado.ioloop.IOLoop.instance().add_callback_from_signal(
                lambda: tornado.ioloop.IOLoop.instance().stop())

    def host_info_task(self):
        host_info = PushData()
        host_info.source_mac_address = self.bat_mac
        host_info.add_data_block(66, 0, self.bat_addr)

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(options.socket_address)
            s.sendall(bytes(host_info))

    def start(self):
        server = HTTPServer(self)
        server.bind(8888, address=self.web_addr)
        server.start(0)

        # This should really point to a task queue
        tornado.ioloop.PeriodicCallback(self.host_info_task, 5000).start()
        tornado.ioloop.IOLoop.current().start()


def main():
    options.parse_command_line()
    Application().start()
