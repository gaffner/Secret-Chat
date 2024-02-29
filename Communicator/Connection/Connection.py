from pydantic import BaseModel


class Connection(BaseModel):
    is_server: bool
