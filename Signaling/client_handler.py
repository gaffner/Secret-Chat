import socket
import json

from typing import Tuple

# save the state of the current connected peer
peer: Tuple[socket.socket, str, int] = ()


def get_signal_message(ip, port):
    return json.dumps({
        'ip': ip,
        'port': port
    }).encode()


def handle_client(sock: socket.socket):
    try:
        message = json.loads(sock.recv(1024))
        ip, port = message['ip'], message['port']
        global peer

        # if a peer already connected, send his details
        if peer:
            print(f'Sending first peer information to second peer: ({peer[1]}, {peer[2]})')
            sock.send(get_signal_message(peer[1], peer[2]))

            print(f'Sending second peer information to first peer: ({ip}, {port})')
            peer[0].send(get_signal_message(ip, port))

        # change the peer to be the current peer
        peer = (sock, ip, port)

    except json.JSONDecodeError:
        print(f'Unable to parse message')
