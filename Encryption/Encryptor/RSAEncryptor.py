import rsa
import secrets
from typing import Generator
from Crypto.Cipher import AES


from Encryption.Encryptor import Encryptor
from Encryption.Configuration import RSAConfiguration
from Settings import SETTINGS


class RSAEncryptor(Encryptor):
    def __init__(self, encryption: RSAConfiguration):
        super().__init__(encryption)
        self.is_initiator = encryption.is_initiator
        self.aes_cipher = None
        self.keys_setup()

    @property
    def full_session_key(self):
        return self._encryption.session_key + self.aes_cipher.nonce

    @property
    def private_key(self):
        return self._encryption.private_key.save_pkcs1()

    @property
    def public_key(self):
        return self._encryption.public_key.save_pkcs1()

    @property
    def encrypted_session_key(self):
        return rsa.encrypt(self.full_session_key, self._encryption.public_key)

    def set_public_key(self, public_key: bytes):
        self._encryption.public_key = rsa.PublicKey.load_pkcs1(public_key)

    def set_decrypted_session_key(self, encrypted_session_key: bytes):
        full_session_key = rsa.decrypt(encrypted_session_key, self._encryption.private_key)
        session_key, nonce = full_session_key[0:16], full_session_key[16:]

        self._encryption.session_key, self._encryption.nonce = session_key, nonce
        self.aes_cipher = AES.new(session_key, AES.MODE_EAX, nonce=nonce)

    def keys_setup(self):
        if self.is_initiator:
            self.generate_rsa_keys()
        else:
            self.generate_session_key()

    def generate_rsa_keys(self):
        self._encryption.public_key, self._encryption.private_key = rsa.newkeys(SETTINGS['encryption']['bits'])

    def generate_session_key(self):
        self._encryption.session_key = secrets.token_bytes(SETTINGS['encryption']['session']['key length'])
        self.aes_cipher = AES.new(self._encryption.session_key, AES.MODE_EAX)
        self._encryption.nonce = self.aes_cipher.nonce

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

    def encrypt(self, data: bytes) -> bytes:
        return self.aes_cipher.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        cipher = AES.new(self._encryption.session_key, AES.MODE_EAX, nonce=self._encryption.nonce)
        return cipher.decrypt(data)
