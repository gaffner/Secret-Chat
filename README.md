# Secret Chat

End to End encrypted and modular chat, with the ability to support a
variety of communication and encryption types.

### Supported communications:

* <b>NAT Hollowing</b> - Peer to Peer Communication over UDP socket. The server hollows his NAT table,
  and then the client communicates to him over this "Hole". This communication mode allows peers who are behind
  NAT Tables (like most of the end users) communicate directly, without the need of a middle server, and therefore the
  most secured.
  <br><br>

> [!NOTE]
> In order to use this communication technique, one needs to set up the <i>Signaling Server</i>, located inside the
> `Signaling` directory, on a server with at least one port exposed to the internet (for example, VPS).
> The purpose of this server is to coordinate the NAT hollowing process between the two peers. Currently,
> the implemented signaling server is just a POC.

![image](https://i.imgur.com/1RH4oua.png)

* <b>Client Server Architecture</b> - Regular Client-Server mode, over <i>TCP</i> socket (just called `TCP` in
  the code for simpler naming) exists in the program to show her ability to be modular, and also to test other
  modules (currently only encryption-related) without the need to use the more complicated way of communication, UDP
  Hole
  punching.
  ![image](https://i.imgur.com/SP9BrSt.png)

### Supported Encryption

* <b>RSA</b> - the recommended way of encryption. This encryption uses RSA for the key exchange and then uses AES
  to encrypt the session communication. All the information needed in order to encrypt the session is exchanged during
  the
  handshake process. This process goes as follows:
    1. The server generates a pair of RSA keys, private and public
    2. The client generates 16 bytes of symmetric AES key
    3. The server sends the public key to the client
    4. The client encrypts his session key using the given public key and sends the encrypted result to the server
    5. The server decrypts the encrypted session key using its private key, and from now on the communication will be
       encrypted using this key

![image](https://i.imgur.com/QjfOJKK.png)

* <b>Pseudo Encryption</b> - Used mostly for communication tests, without the need to use the complex RSA encryption.

### How to use it?

```bash
pip install -r requirments.txt
```
```bash
python -m examples.server

2024-03-12 18:56:06.352 INFO UDPCommunicator - send_signals: Connecting to signaling server
2024-03-12 18:56:06.568 DEBUG connectionpool - _new_conn: Starting new HTTP connection (1): ifconfig.me:80
2024-03-12 18:56:06.739 DEBUG connectionpool - _make_request: http://ifconfig.me:80 "GET / HTTP/1.1" 200 14
2024-03-12 18:56:06.740 INFO UDPCommunicator - send_signals: Sent ip and port to signaling server
2024-03-12 18:56:32.467 INFO UDPCommunicator - send_signals: Received peer {'ip': '98.137.11.164', 'port': 17228} from signaling server
2024-03-12 18:56:37.601 INFO UDPCommunicator - _server_udp_hollow: Received b'Hello' from ('98.137.11.164', 17228)
2024-03-12 18:56:37.601 INFO Chat - do_handshake: Starting handshake process
2024-03-12 18:56:37.645 INFO Chat - do_handshake: Sending handshake stage from encryptor to peer
2024-03-12 18:56:37.720 INFO Chat - do_handshake: Received handshake stage from client, send it to encryptor

Client: Hello from client
You: Hello from server
```
```bash
python -m examples.client

2024-03-12 09:56:31.357 INFO UDPCommunicator - send_signals: Connecting to signaling server
2024-03-12 09:56:31.732 DEBUG connectionpool - _new_conn: Starting new HTTP connection (1): ifconfig.me:80
2024-03-12 09:56:32.186 DEBUG connectionpool - _make_request: http://ifconfig.me:80 "GET / HTTP/1.1" 200 11
2024-03-12 09:56:32.186 INFO UDPCommunicator - send_signals: Sent ip and port to signaling server
2024-03-12 09:56:32.435 INFO UDPCommunicator - send_signals: Received peer {'ip': '140.82.121.3', 'port': 17226} from signaling server
2024-03-12 09:56:37.561 INFO UDPCommunicator - _client_udp_hollow: Received b'Hello' from ('140.82.121.3', 17226)
2024-03-12 09:56:37.561 INFO Chat - do_handshake: Starting handshake process
2024-03-12 09:56:37.592 INFO Chat - do_handshake: Received handshake stage from client, send it to encryptor
2024-03-12 09:56:37.639 INFO Chat - do_handshake: Sending handshake stage from encryptor to peer

You: Hello from client
Client: Hello from server
```

The `server.py` and `client.py` in the examples directory simulates
server and a client, using the UDP Hole Punching communication method + RSA encryption.
make sure the signaling server is up and running, and the address of it is written in the `settings` file under
the `signaling server` property.

```bash
python Signaling/main.py # POC
```

of course, the communication type and encryption type can be changed very simply. for example,
initialize chat with UDP communication and RSA encryption:

```python
from Chat import Chat
from Interactor.ConsoleInteractor import ConsoleInteractor

from Communication.Connection import UDPConnection
from Encryption.Configuration import RSAConfiguration

from Settings import SETTINGS

# initialize configurations for communication and encryption
connection = UDP
connection(is_server=False,
           signaling_server=('signaling-server.com', 8080))
encryption = RSAConfiguration(is_initiator=True)

# initialize chat and wait for connections
chat = Chat(connection=connection, encryption=encryption)
chat.wait_for_connection()

# Initialize and start the interactor
interactor = ConsoleInteractor(chat)
interactor.interaction_loop()



```

## Secret Chat Components

| Component    |                                                                                                 Purpose                                                                                                 |                       Implementations |
|--------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|--------------------------------------:|
| Communicator |                                                 In charge of communicating with the target peer. The<br/>only component which uses network capabilities                                                 |   TCPCommunicator<br/>UDPCommunicator |
| Encryptor    |                                                               In charge of encrypting and decrypting<br/>incoming and outcoming messages                                                                |      RSAEncryptor<br/>PseudoEncryptor |
| Interactor   | In charge of communicating with the end user. Currently, the only implementation is the `ConsoleInteractor`, but other type of interactions (for example `GraphicInteractor`) can easily be implemented |                     ConsoleInteractor |
| Chat         |                      In charge of the end-to-end message process. This component gathers most of the other components and uses them when needed. Contained inside the `Interactor`                      |                                  Chat |

The components of the project also described in the bellow flowchart:
![image](https://i.imgur.com/UYFOYKI.png)
