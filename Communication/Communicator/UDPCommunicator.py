import requests
import socket
import logging
import json
import time

from Communication.Communicator import Communicator
from Communication.Connection import UDPConnection

from Settings import SETTINGS


class UDPCommunicator(Communicator):
    def __init__(self, connection: UDPConnection):
        super().__init__(connection)
        self._signaling_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if not connection.is_server:
            connection.source = ('0.0.0.0', SETTINGS['communication']['udp']['communication port'])

    def wait_for_connection(self):
        self.send_signals()
        self.udp_hole_punching()

    def udp_hole_punching(self):
        # bind the socket to the given source port
        self._socket.bind(self._connection.source)

        if not self._connection.is_server:
            self._socket.connect(self._connection.destination)

        # hollow the NAT table and wait for
        # the peer to hollow his NAT as well
        self._socket.sendto(b'udp puncher', self._connection.destination)
        time.sleep(SETTINGS['communication']['udp']['sleep interval'])

        self._socket.sendto(b'Hello', self._connection.destination)

        data, address = self._socket.recvfrom(self._buffer_size)
        logging.getLogger('Chat').info(f"Received {data} from {address}")

    def send_signals(self):
        logging.getLogger('Chat').info(f"Connecting to signaling server")
        self._signaling_socket.connect(self._connection.signaling_server)
        self._signaling_socket.send(json.dumps({
            'ip': UDPCommunicator.get_ip(),
            'port': self._connection.source[1]
        }).encode())
        logging.getLogger('Chat').info(f"Sent ip and port to signaling server")

        peer = json.loads(self._signaling_socket.recv(SETTINGS['communication']['buffer size']))
        logging.getLogger('Chat').info(f"Received peer {peer} from signaling server")
        self._connection.destination = (peer['ip'], peer['port'])

    def send(self, data: bytes):
        self._socket.sendto(data, self._connection.destination)

    def receive(self) -> bytes:
        return self._socket.recv(self._buffer_size)

    @staticmethod
    def get_ip():
        settings_ip = SETTINGS['communication']['udp']['external ip']

        if settings_ip:
            return settings_ip
        else:
            return requests.get(SETTINGS['communication']['udp']['resolve service']).content.decode('utf8')
