import socket
import logging

from Communication.Communicator import Communicator
from Communication.Connection import TCPConnection


class TCPCommunicator(Communicator):

    def __init__(self, connection: TCPConnection):
        super().__init__(connection)
        self.socket: socket.socket
        self._listener: socket.socket
        self._init_socket()

    def _init_socket(self):
        """
        init socket according to the mode (server or client)
        """
        if self._connection.is_server:
            self._init_server()
        else:
            self._init_client()

    def _init_server(self):
        """
        init socket for server mode
        """
        self._listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._listener.bind(self._connection.address)
        self._listener.listen()
        logging.getLogger('Chat').info(f"Starting to listen on address {self._connection.address}")

    def _init_client(self):
        """
        init socket for client mode
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # noinspection PyAttributeOutsideInit
    def wait_for_connection(self):
        """
        blocking function, waits until new connection
        """
        if self._connection.is_server:
            logging.getLogger('Chat').debug(f'Waiting for new connection, server mode: {self._connection.is_server}')
            client_socket, client_address = self._listener.accept()
            logging.getLogger('Chat').debug(f'Accepted new connection from client {client_address}')
            self.socket = client_socket
        else:
            self.socket.connect(self._connection.address)
            logging.getLogger('Chat').info(f'Connected to server {self._connection.address}')

    def send(self, data: bytes):
        self.socket.send(data)

    def receive(self) -> bytes:
        return self.socket.recv(self._buffer_size)
