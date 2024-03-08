from Communication.Connection import Connection
from Communication.Factory.CommunicationMapping import mapping


class CommunicatorFactory:
    @staticmethod
    def create(connection: Connection):
        return mapping[type(connection)](connection)
