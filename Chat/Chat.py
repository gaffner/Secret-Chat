import logging

from Settings import SETTINGS

from Communication.Communicator import Communicator
from Communication.Connection import Connection
from Communication.Factory import CommunicatorFactory

from Encryption.Encryptor import Encryptor
from Encryption.Configuration import EncryptionConfiguration
from Encryption.Factory import EncryptorFactory

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )


class Chat:
    def __init__(self, connection: Connection, encryption: EncryptionConfiguration):
        self._communicator: Communicator = CommunicatorFactory.create(connection)
        self._encryptor: Encryptor = EncryptorFactory.create(encryption)
        self._encoding = SETTINGS['Encoding']
        self.is_server = connection.is_server

    def wait_for_connection(self):
        self._communicator.wait_for_connection()

    def send_text(self, text: str):
        encrypted_data = self._encryptor.encrypt(text.encode(self._encoding))
        self._communicator.send(encrypted_data)

    def receive_text(self) -> str:
        encrypted_data = self._communicator.receive()
        return self._encryptor.decrypt(encrypted_data).decode(self._encoding)
