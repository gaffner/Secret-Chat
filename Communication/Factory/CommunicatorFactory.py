from Communication.Connection import Connection
from Communication.Factory.Mapping import mapping


class CommunicatorFactory:
    @staticmethod
    def create(connection: Connection):
        return mapping[type(connection)](connection)
