import socket

from Communicator import Communicator
from Communicator.Connection import TCPConnection


class TCPCommunicator(Communicator):
    buffer_size: int = 1024

    def __init__(self, connection: TCPConnection):
        super().__init__(connection)
        self.socket: socket.socket
        self.listener: socket.socket
        self._init_socket()

    def _init_socket(self):
        """
        init socket according to the mode (server or client)
        """
        if self.connection.is_server:
            self._init_server()
        else:
            self._init_client()

    def _init_server(self):
        """
        init socket for server mode
        """
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(self.connection.address)
        self.listener.listen()
        self.logger.info(f"Starting to listen on address {self.connection.address}")

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
        if self.connection.is_server:
            self.logger.debug(f'Waiting for new connection, server mode: {self.connection.is_server}')
            client_socket, client_address = self.listener.accept()
            self.logger.debug(f'Accepted new connection from client {client_address}')
            self.socket = client_socket
        else:
            self.socket.connect(self.connection.address)
            self.logger.info(f'Connected to server {self.connection.address}')

    def send(self, data: bytes):
        self.socket.send(data)

    def receive(self) -> bytes:
        return self.socket.recv(self.buffer_size)
