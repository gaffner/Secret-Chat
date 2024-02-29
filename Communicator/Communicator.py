from abc import ABC, abstractmethod
from Connection import Connection
import logging


class Communicator(ABC):
    def __init__(self, connection: Connection):
        self.connection = connection
        self.logger = logging.getLogger('Chat')

    @abstractmethod
    def send(self, data: bytes) -> None:
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
