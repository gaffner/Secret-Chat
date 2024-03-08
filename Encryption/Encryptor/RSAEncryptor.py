import rsa
import secrets
from typing import Generator

from Encryption.Encryptor import Encryptor
from Encryption.Configuration import RSAConfiguration
from Settings import SETTINGS


class RSAEncryptor(Encryptor):
    def __init__(self, encryption: RSAConfiguration):
        super().__init__(encryption)
        self.is_initiator = encryption.is_initiator
        self.keys_setup()

    @property
    def session_key(self):
        return self._encryption.session_key

    @property
    def private_key(self):
        return self._encryption.private_key.save_pkcs1()

    @property
    def public_key(self):
        return self._encryption.public_key.save_pkcs1()

    @property
    def encrypted_session_key(self):
        return rsa.encrypt(self.session_key, self._encryption.public_key)

    def set_public_key(self, public_key: bytes):
        self._encryption.public_key = rsa.PublicKey.load_pkcs1(public_key)

    def set_decrypted_session_key(self, encrypted_session_key: bytes):
        self._encryption.session_key = rsa.decrypt(encrypted_session_key, self._encryption.private_key)

    def keys_setup(self):
        if self.is_initiator:
            self.generate_rsa_keys()
        else:
            self.generate_session_key()

    def generate_rsa_keys(self):
        self._encryption.public_key, self._encryption.private_key = rsa.newkeys(SETTINGS['encryption']['bits'])

    def generate_session_key(self):
        # self._encryption.session_key = secrets.token_bytes(SETTINGS['encryption']['session']['key length'])
        self._encryption.session_key = b'Gefen'

    @property
    def handshake(self) -> Generator:
        """
        returns the handshake sequence of the Asymmetric Encryptor.
        each item of the list is lambda object, which will be executed on each
        iteration of the generator returns from the function. this allows the encryptor
        to set values according to some calculation of the peer data, and then return it
        on the next message. for example, encrypting the session key with the given public key.
        :return: Generator
        """
        if self.is_initiator:
            stages = [lambda: self.public_key, lambda: self.set_decrypted_session_key]
        else:
            stages = [lambda: self.set_public_key, lambda: self.encrypted_session_key]

        for stage in stages:
            yield stage()

    @staticmethod
    def xor_bytes(data: bytes, key: bytes):
        encrypted = []

        for i in range(len(data)):
            encrypted.append(data[i] ^ key[i % len(key)])

        return bytes(encrypted)

    def encrypt(self, data: bytes) -> bytes:
        return RSAEncryptor.xor_bytes(data, self.session_key)

    def decrypt(self, data: bytes) -> bytes:
        return RSAEncryptor.xor_bytes(data, self.session_key)
