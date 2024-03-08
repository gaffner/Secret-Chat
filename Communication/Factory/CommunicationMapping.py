from Communication.Communicator import TCPCommunicator
from Communication.Communicator import UDPCommunicator

from Communication.Connection import TCPConnection
from Communication.Connection import UDPConnection

mapping = {
    TCPConnection: TCPCommunicator,
    UDPConnection: UDPCommunicator
}