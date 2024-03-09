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

    def wait_for_connection(self):
        logging.getLogger('Chat').info(f"Connecting to signaling server")
        self._signaling_socket.connect(self._connection.signaling_server)
        self._signaling_socket.send(json.dumps({
            'ip': UDPCommunicator.get_ip(),
            'port': SETTINGS['communication']['udp']['communication port']
        }).encode())
        logging.getLogger('Chat').info(f"Sent ip and port to signaling server")

        peer = json.loads(self._signaling_socket.recv(SETTINGS['communication']['buffer size']))
        logging.getLogger('Chat').info(f"Received peer {peer} from signaling server")
        self._connection.destination = (peer['ip'], peer['port'])

    def udp_hole_punching(self):
        # init UDP server if needed
        if self._connection.is_server:
            self._socket.bind(self._connection.source)

        # hollow the NAT table and wait for
        # the peer to hollow his NAT as well
        self._socket.sendto(b'udp puncher', self._connection.destination)
        time.sleep(SETTINGS['communication']['udp']['sleep interval'])

        data, address = self._socket.recvfrom(self._buffer_size)
        logging.getLogger('Chat').info(f"Received {data} from {address}")

    def send(self, data: bytes):
        self._socket.send(data)

    def receive(self) -> bytes:
        return self._socket.recv(self._buffer_size)

    @staticmethod
    def get_ip():
        return requests.get(SETTINGS['communication']['udp']['resolve service']).content.decode('utf8')
