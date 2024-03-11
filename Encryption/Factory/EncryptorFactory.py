from Encryption.Configuration import EncryptionConfiguration
from Encryption.Factory.Mapping import mapping


class EncryptorFactory:
    @staticmethod
    def create(encryption: EncryptionConfiguration):
        return mapping[type(encryption)](encryption)
