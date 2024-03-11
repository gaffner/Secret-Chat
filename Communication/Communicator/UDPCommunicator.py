import requests
import socket
import logging
import json
import time

from Communication.Communicator import Communicator, UDPConsts
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
        """
        Make sure the UDP communication will work properly,
        by sending UDP Hollow packet through the NAT  in case of a server,
        or just send 'Hello' message in case of a client, and wait for corresponding Hello.
        """

        self._socket.bind(self._connection.source)

        if self._connection.is_server:
            self._server_udp_hollow()
        else:
            self._client_udp_hollow()

    def _server_udp_hollow(self):
        """
        Hollow the NAT Table and wait for the client message
        """
        # Send the Hollow message
        self._socket.sendto(UDPConsts.HollowMessage, self._connection.destination)

        # Wait for client Hello
        data, address = self._socket.recvfrom(self._buffer_size)
        logging.getLogger('Chat').info(f"Received {data} from {address}")

        # Send the client Hello back
        self._socket.sendto(UDPConsts.Hello, self._connection.destination)

    def _client_udp_hollow(self):
        """
        Send message to the server behind his hollowed NAT
        """
        # Connect to target UDP server
        self._socket.connect(self._connection.destination)

        # send the server the 'Hello' Message. assuming his NAT Table is already opened
        self._socket.sendto(UDPConsts.Hello, self._connection.destination)

        # Wait for server 'hello' Message
        data, address = self._socket.recvfrom(self._buffer_size)
        logging.getLogger('Chat').info(f"Received {data} from {address}")

    def send_signals(self):
        """
        send to the signaling server our external ip address and source port,
        and get in return the external address and source port of the peer.
        """

        # Connect to signaling server
        logging.getLogger('Chat').info(f"Connecting to signaling server")
        self._signaling_socket.connect(self._connection.signaling_server)

        # send our address information to the signaling server
        self._signaling_socket.send(json.dumps({
            'ip': UDPCommunicator.get_ip(),
            'port': self._connection.source[1]
        }).encode())
        logging.getLogger('Chat').info(f"Sent ip and port to signaling server")

        # Parse the response and set the destination accordingly
        peer = json.loads(self._signaling_socket.recv(SETTINGS['communication']['buffer size']))
        logging.getLogger('Chat').info(f"Received peer {peer} from signaling server")
        self._connection.destination = (peer['ip'], peer['port'])

    def send(self, data: bytes):
        self._socket.sendto(data, self._connection.destination)

    def receive(self) -> bytes:
        return self._socket.recv(self._buffer_size)

    @staticmethod
    def get_ip():
        """
        Get the external ip by local settings or
        if not exists by online resolve service.
        """
        settings_ip = SETTINGS['communication']['udp']['external ip']

        if settings_ip:
            return settings_ip
        else:
            return requests.get(SETTINGS['communication']['udp']['resolve service']).content.decode('utf8')
