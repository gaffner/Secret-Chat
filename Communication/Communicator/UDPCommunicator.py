import requests
import socket
import json

from Communication.Communicator import Communicator
from Communication.Connection import UDPConnection

from Settings import SETTINGS


class UDPCommunicator(Communicator):
    def __init__(self, connection: UDPConnection):
        super().__init__(connection)
        self.signaling_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def wait_for_connection(self):
        self.signaling_socket.connect(self._connection.signaling_server)
        self.signaling_socket.send(json.dumps({
            'ip': UDPCommunicator.get_ip(),
            'port': SETTINGS['udp']['communication port']
        }).encode())

    def send(self, data: bytes):
        pass

    def receive(self) -> bytes:
        pass

    @staticmethod
    def get_ip():
        return requests.get('http://ifconfig.me').content.decode('utf8')
