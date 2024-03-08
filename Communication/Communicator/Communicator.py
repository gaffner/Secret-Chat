from abc import ABC, abstractmethod
from Communication.Connection import Connection
from Settings import SETTINGS


class Communicator(ABC):
    def __init__(self, connection: Connection):
        self._connection = connection
        self._buffer_size = SETTINGS['Buffer size']

    @abstractmethod
    def wait_for_connection(self):
        pass

    @abstractmethod
    def send(self, data: bytes):
        """
        send bytes to target user
        """
        pass

    @abstractmethod
    def receive(self) -> bytes:
        """
        receive bytes from target user
        :return:
        """
        pass
