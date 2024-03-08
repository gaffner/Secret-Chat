from Encryption.Configuration import EncryptionConfiguration
from Encryption.Factory.EncryptionMapping import mapping


class EncryptorFactory:
    @staticmethod
    def create(encryption: EncryptionConfiguration):
        return mapping[type(encryption)](encryption)
