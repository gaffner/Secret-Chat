import logging
from abc import ABC, abstractmethod

from Communicator.Communicator import Communicator
from Communicator.Connection import Connection
from Encryptor.Encryptor import Encryptor
from Encryptor.Factory import EncryptorFactory
from Encryptor.Configuration import Encryption

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )


class Chat(ABC):
    def __init__(self, connection: Connection, encryption: Encryption):
        self._communicator: Communicator = Communicator(connection)
        self._encryptor: Encryptor = EncryptorFactory.create(encryption)

    def send_data(self, data: bytes):
        encrypted_data = self._encryptor.encrypt(data)

        self._communicator.send(encrypted_data)

    def receive_data(self) -> bytes:
        encrypted_data = self._communicator.receive()

        return self._encryptor.decrypt(encrypted_data)
