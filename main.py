from Chat import Chat
from Interactor.ConsoleInteractor import ConsoleInteractor

from Communication.Connection import TCPConnection
from Encryption.Configuration import AsymmetricConfiguration


def main():
    # initialize configurations for communication and encryption
    connection = TCPConnection(is_server=True, address=('0.0.0.0', 1726))
    encryption = AsymmetricConfiguration(is_initiator=True)

    # initialize chat and wait for connections
    chat = Chat(connection=connection, encryption=encryption)
    chat.wait_for_connection()

    # initialize and start interactor
    interactor = ConsoleInteractor(chat)
    interactor.interaction_loop()


if __name__ == '__main__':
    main()
