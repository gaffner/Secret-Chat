from abc import ABC, abstractmethod
from Encryption.Configuration import EncryptionConfiguration


class Encryptor(ABC):
    def __init__(self, encryption: EncryptionConfiguration):
        self.encryption = encryption

    @abstractmethod
    def encrypt(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, data: bytes) -> bytes:
        pass
