import socket
import threading

from client_handler import handle_client

LISTENING_ADDRESS = ('0.0.0.0', 8080)


def main():
    """
    The job of this program is simply to use as signaling server for 2 peers.
    it does not handle multi clients situation, identity managements, authentication, etc.
    It's only job is to be 'quick and dirty', basically POC of signaling server.
    of curse there is much more work on it to make it fully functional and scalable.
    :return:
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(LISTENING_ADDRESS)
    server_socket.listen()

    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Connection from {client_address} established')

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


if __name__ == '__main__':
    main()
