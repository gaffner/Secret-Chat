from pydantic import BaseModel


class EncryptionConfiguration(BaseModel):
    is_initializer: bool
