from abc import ABC, abstractmethod


class Encryptor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def encrypt(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, data: bytes) -> bytes:
        pass
