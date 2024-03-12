from Chat import Chat
from Interactor.ConsoleInteractor import ConsoleInteractor

from Communication.Connection import UDPConnection
from Encryption.Configuration import RSAConfiguration

from Settings import SETTINGS


def main():
    # initialize configurations for communication and encryption
    connection = UDPConnection(is_server=False,
                               signaling_server=(SETTINGS['communication']['udp']['signaling server'], 8080))
    encryption = RSAConfiguration(is_initiator=False)

    # initialize chat and wait for connections
    chat = Chat(connection=connection, encryption=encryption)
    chat.wait_for_connection()

    # initialize and start interactor
    interactor = ConsoleInteractor(chat)
    interactor.interaction_loop()


if __name__ == '__main__':
    main()
