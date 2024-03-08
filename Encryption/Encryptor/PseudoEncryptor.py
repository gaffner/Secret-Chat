from typing import Generator

from Encryption.Encryptor import Encryptor


class PseudoEncryptor(Encryptor):

    @property
    def handshake(self) -> Generator:
        yield []

    def encrypt(self, data: bytes) -> bytes:
        return data

    def decrypt(self, data: bytes) -> bytes:
        return data
