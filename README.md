# Secret Chat

End to End encrypted and modular chat, with the ability to support a
variety of communication and encryption types.

### Supported communications:

* <b>Client Server Architecture</b> - Regular Client-Server mode, over <i>TCP</i> socket (called just `TCP` in
  the code for simpler name) Exists in the program only to show her ability to be modular, and also to test other
  modules
  (currently only encryption-related) without the need to use the more complicated way of communication, UDP Hole
  punching.
  ![image](https://i.imgur.com/SP9BrSt.png)
* <b>NAT Hollowing</b> - Peer to Peer Communication over UDP socket. The "Server" Hollow his NAT table,
  and then the "client" communicate to him over this "Hole". This communication mode allows peers that are behind
  NAT Tables (like most of the end users) to communicate directly, without the need of middle server, and therefor the
  most secured.
  <br><br>

> [!NOTE]
> In order to use this communication technique, one need to setup the <i>Signaling Server</i>, located inside the
> `Signaling` directory, on a server with at least one port exposed to the internet (for example, VPS).
> The purpose of this server is to coordinate the NAT Hollowing porcess between the two peers. Currently, the code of
> this
> signaling server is basically a POC, and therefore not stable and scalable. It can easily be replaced by another
> signaling server,
> as it's protocol will be described later.
>
![image](https://i.imgur.com/1RH4oua.png)

### Supported Encryption

* <b>RSA</b> - the recommended way of encryption. This encryption usa RSA for the keys exchange part, and then using AES
  to encrypt the session communication. All the information needed in order to encrypt the session is exchanged during
  the
  handhskae process, and it goes as follows:
    1. The server generate pair of RSA keys, private and public
    2. The client generate 16 bytes of symmetric AES key
    3. The server send the public key to the client
    4. The client encrypt his session key using the given public key, and send the encrypted result to the server
    5. The server decrypt the encrypted session key using his private key, and from now on the communication will be
       encrypted using this key

![image](https://i.imgur.com/QjfOJKK.png)

* <b>Pseudo Encryption</b> - Used mostly for communication tests, without the need to use the complex RSA encryption.

### How to use?

```bash
pip install -r requirments.txt

python -m examples.server
python -m examples.client
```

The `server.py` and `client.py` in the examples directory simulates
Server and a Client, using the UDP Hole Punching communication method + RSA encryption.
Make sure the signaling server is up and running, and his address is written in the `settings` file under
`signaling server` property.

```bash
python Signaling/main.py # The signaling POC Server
```

of curse the communication type and encryption type can be changed very simply. For example,
setting communication to be UDP and RSA encryption:

```python
from Chat import Chat
from Interactor.ConsoleInteractor import ConsoleInteractor

from Communication.Connection import UDPConnection
from Encryption.Configuration import RSAConfiguration

from Settings import SETTINGS

# initialize configurations for communication and encryption
connection = UDPConnection(is_server=False,
                           signaling_server=('signaling-server.com', 8080))
encryption = RSAConfiguration(is_initiator=True)

# initialize chat and wait for connections
chat = Chat(connection=connection, encryption=encryption)
chat.wait_for_connection()

# initialize and start interactor
interactor = ConsoleInteractor(chat)
interactor.interaction_loop()



```

## Secret Chat Components

| Component    |                                                                                                              Job                                                                                                               |                     Implementations |
|--------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|------------------------------------:|
| Communicator |                                                             In charge of communicate with the target peer.The<br/>only component which using network capabilities                                                              | TCPCommunicator<br/>UDPCommunicator |
| Encryptor    |                                                                            In charge of encrypted and decrypting<br/>messages coming from the peer                                                                             |    RSAEncryptor<br/>PseudoEncryptor |
| Interactor   | In charge of communicate with the end user. Currently the only implementation is the `ConsoleInteractor`,but other interactors (for example `GraphicInteractor`, or `ReactInteractor`, or whatever) can easily by implemented. |                   ConsoleInteractor |
| Chat         |                                In charge of the end to end message process. This component gathers most of the other components, and use them when needed. Contained inside the `Interactor` .                                 |                                Chat |

The component of the project also described in the bellow flowchart:
![image](https://i.imgur.com/UYFOYKI.png)
