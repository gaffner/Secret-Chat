from Encryption.Encryptor import Encryptor


class PseudoEncryptor(Encryptor):

    def encrypt(self, data: bytes) -> bytes:
        return data

    def decrypt(self, data: bytes) -> bytes:
        return data
