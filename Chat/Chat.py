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
        self._encoding = SETTINGS['communication']['encoding']
        self.is_server = connection.is_server

    def wait_for_connection(self):
        """
        iterate over the handshake stages of the given encryptor.
        if the stage is function - execute it with the peer message.
        if the stage is bytes - send it to the peer.
        :return:
        """
        self._communicator.wait_for_connection()
        self.do_handshake()

    def do_handshake(self):
        logging.getLogger('Chat').info(f"Starting handshake process")
        for stage in self._encryptor.handshake:
            if callable(stage):
                peer_message = self._communicator.receive()
                logging.getLogger('Chat').info(f"Received handshake stage from client, send it to encryptor")
                stage(peer_message)
            else:
                logging.getLogger('Chat').info(f"Sending handshake stage from encryptor to peer")
                self._communicator.send(stage)

    def send_text(self, text: str):
        encrypted_data = self._encryptor.encrypt(text.encode(self._encoding))
        self._communicator.send(encrypted_data)

    def receive_text(self) -> str:
        encrypted_data = self._communicator.receive()
        decrypted = self._encryptor.decrypt(encrypted_data)

        try:
            return decrypted.decode(self._encoding)
        except UnicodeDecodeError:
            logging.getLogger('Chat').error(f"Error trying convert {decrypted} to {self._encoding} format")
