from pydantic import BaseModel


class EncryptionConfiguration(BaseModel):
    is_initiator: bool
