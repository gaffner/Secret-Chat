from Chat import Chat
from Interactor.ConsoleInteractor import ConsoleInteractor

from Communication.Connection import TCPConnection
from Encryption.Configuration import PseudoConfiguration


def main():
    connection = TCPConnection(is_server=True, address=('0.0.0.0', 1726))
    encryption = PseudoConfiguration(is_initializer=True)
    chat = Chat(connection=connection, encryption=encryption)
    interactor = ConsoleInteractor(chat)

    interactor.interaction_loop()


if __name__ == '__main__':
    main()
