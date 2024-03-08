from Encryption.Configuration import EncryptionConfiguration


class RSAConfiguration(EncryptionConfiguration):
    private_key: bytes = None
    public_key: bytes = None
    session_key: bytes = None
