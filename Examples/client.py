from Chat import Chat
from Interactor.ConsoleInteractor import ConsoleInteractor

from Communication.Connection import TCPConnection
from Encryption.Configuration import RSAConfiguration


def main():
    # initialize configurations for communication and encryption
    connection = TCPConnection(is_server=False, address=('127.0.0.1', 1726))
    encryption = RSAConfiguration(is_initiator=False)

    # initialize chat and wait for connections
    chat = Chat(connection=connection, encryption=encryption)
    chat.wait_for_connection()

    # initialize and start interactor
    interactor = ConsoleInteractor(chat)
    interactor.interaction_loop()


if __name__ == '__main__':
    main()
