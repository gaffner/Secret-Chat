from Encryption.Encryptor import Encryptor
from Encryption.Configuration import AsymmetricConfiguration


class AsymmetricEncryptor(Encryptor):
    def __init__(self, encryption: AsymmetricConfiguration):
        super().__init__(encryption)

    def encrypt(self, data: bytes) -> bytes:
        pass

    def decrypt(self, data: bytes) -> bytes:
        pass
