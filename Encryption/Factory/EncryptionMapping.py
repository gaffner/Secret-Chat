from Encryption.Encryptor import PseudoEncryptor
from Encryption.Encryptor import AsymmetricEncryptor

from Encryption.Configuration import AsymmetricConfiguration
from Encryption.Configuration import PseudoConfiguration

mapping = {
    AsymmetricConfiguration: AsymmetricEncryptor,
    PseudoConfiguration: PseudoEncryptor
}