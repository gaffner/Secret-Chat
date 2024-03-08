from abc import ABC, abstractmethod
from typing import Generator
from Encryption.Configuration import EncryptionConfiguration


class Encryptor(ABC):
    def __init__(self, encryption: EncryptionConfiguration):
        self._encryption = encryption

    @abstractmethod
    @property
    def handshake(self) -> Generator:
        pass

    @abstractmethod
    def encrypt(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, data: bytes) -> bytes:
        pass
