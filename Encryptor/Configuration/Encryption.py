from enum import Enum

from Encryptor.PseudoEncryptor import PseudoEncryptor
from Encryptor.AsymetricEncryptor import AsymmetricEncryptor


class Encryption(Enum):
    PSEUDO = PseudoEncryptor.encryption
    ASYMMETRIC = AsymmetricEncryptor.encryption
