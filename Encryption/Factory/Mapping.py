from Encryption.Encryptor import PseudoEncryptor
from Encryption.Encryptor import RSAEncryptor

from Encryption.Configuration import RSAConfiguration
from Encryption.Configuration import PseudoConfiguration

mapping = {
    RSAConfiguration: RSAEncryptor,
    PseudoConfiguration: PseudoEncryptor
}