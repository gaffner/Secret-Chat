import socket
from Communicator import Communicator
from Connection import TCPConnection


class TCPCommunicator(Communicator):

    def __init__(self, connection: TCPConnection):
        super().__init__(connection)
        self.socket: socket.socket
        self._init_socket()

    def _init_socket(self):
        """
        init socket according to the mode (server or client)
        """
        if self.connection.is_server:
            self._init_server()

        self._init_client()

    def _init_server(self):
        """
        init socket for server mode
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.connection.address)
        self.socket.listen()
        self.logger.info(f"Starting to listen on address {self.connection.address}")

    def _init_client(self) -> socket.socket:
        """
        init socket for client mode
        """
        pass

    def send(self, data: bytes):
        pass

    def receive(self) -> bytes:
        pass
