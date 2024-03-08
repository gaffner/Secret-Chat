from Communication.Connection import Connection
from typing import Tuple


class TCPConnection(Connection):
    address: Tuple[str, int]
