from Encryption.Configuration import EncryptionConfiguration


class AsymmetricConfiguration(EncryptionConfiguration):
    private_key: bytes
    public_key: bytes
    session_key: bytes
