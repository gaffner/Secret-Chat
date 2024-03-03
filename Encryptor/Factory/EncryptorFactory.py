from Encryptor.AsymetricEncryptor import AsymmetricEncryptor
from Encryptor.PseudoEncryptor import PseudoEncryptor
from Encryptor.Configuration import Encryption


class EncryptorFactory:
    encryption_mapping = {
        Encryption.ASYMMETRIC: AsymmetricEncryptor,
        Encryption.PSEUDO: PseudoEncryptor
    }

    @classmethod
    def create(cls, encryption: Encryption):
        return cls.encryption_mapping[encryption]()
