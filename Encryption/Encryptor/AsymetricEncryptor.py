import rsa
import secrets
from typing import Generator

from Encryption.Encryptor import Encryptor
from Encryption.Configuration import AsymmetricConfiguration
from Settings import SETTINGS


class AsymmetricEncryptor(Encryptor):
    def __init__(self, encryption: AsymmetricConfiguration):
        super().__init__(encryption)
        self.is_initiator = encryption.is_initiator
        self.keys_setup()

    @property
    def session_key(self):
        return

    def set_public_key(self, public_key: bytes):
        self._encryption.public_key = public_key

    def set_session_key(self, session_key: bytes):
        self._encryption.session_key = session_key

    def keys_setup(self):
        if self.is_initiator:
            self.generate_asymmetric_keys()
        else:
            self.generate_session_key()

    def generate_asymmetric_keys(self):
        self._encryption.private_key, self._encryption.public_key = rsa.newkeys(SETTINGS['encryption']['bits'])

    def generate_session_key(self):
        self._encryption.session_key = secrets.token_bytes(SETTINGS['encryption']['session']['key length'])

    @property
    def handshake(self) -> Generator:
        """
        Returns the handshake sequence of the Asymmetric Encryptor.
        Each item of the list is lambda object, which will be executed on each
        iteration of the generator returns from the function. this allows the encryptor
        to set values according to some calculation of the peer data, and then return it
        on the next message. for example, encrypting the session key with the given public key.
        :return: Generator
        """
        if self.is_initiator:
            messages = [lambda: self._encryption.public_key, lambda: self.set_session_key]
        else:
            messages = [lambda: self.set_public_key, lambda: self.session_key]

        for message in messages:
            yield message()

    def encrypt(self, data: bytes) -> bytes:
        pass

    def decrypt(self, data: bytes) -> bytes:
        pass
