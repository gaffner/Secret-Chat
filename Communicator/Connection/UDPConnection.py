from Communicator.Connection import Connection
from typing import Tuple


class UDPConnection(Connection):
    source: Tuple[str, int]
    destination: Tuple[str, int]
    signaling_server: Tuple[str, int]
