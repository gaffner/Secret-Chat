import logging

from Communicator import TCPCommunicator
from Communicator.Connection import TCPConnection

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )

server_config = TCPConnection(address=('localhost', 1726), is_server=True)
server = TCPCommunicator(server_config)
server.wait_for_connection()

while True:
    data = input('Write your text: ')
    server.send(data.encode('ascii'))
    response = server.receive()
    print(f'Client: {response.decode("ascii")}')
