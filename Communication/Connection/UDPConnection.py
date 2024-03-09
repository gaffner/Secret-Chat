from Communication.Connection import Connection
from typing import Tuple


class UDPConnection(Connection):
    source: Tuple[str, int] = None
    destination: Tuple[str, int] = None
    signaling_server: Tuple[str, int]
