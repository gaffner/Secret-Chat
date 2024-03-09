from Communication.Communicator import Communicator
from Communication.Connection import UDPConnection


class UDPCommunicator(Communicator):
    def __init__(self, connection: UDPConnection):
        super().__init__(connection)

    def wait_for_connection(self):
        pass

    def send(self, data: bytes):
        pass

    def receive(self) -> bytes:
        pass
