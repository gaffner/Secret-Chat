# Secret Chat
End to End encrypted and modular chat, with the ability to support a
variety of communication and encryption types.

### Supported communications:
* <b>Client Server Architecture</b> - Regular Client-Server mode, over <i>TCP</i> socket (called just `TCP` in
the code for simpler name) Exists in the program only to show her ability to be modular, and also to test other modules
(currently only encryption-related) without the need to use the more complicated way of communication, UDP Hole punching.
![image](https://i.imgur.com/SP9BrSt.png)
* <b>NAT Hollowing</b> - Peer to Peer Communication over UDP socket. The "Server" Hollow his NAT table,
and then the "client" communicate to him over this "Hole". This communication mode allows peers that are  behind
NAT Tables (like most of the end users) to communicate directly, without the need of middle server, and therefor the most secured.
<br><br>
> [!NOTE]
> In order to use this communication technique, one need to setup the <i>Signaling Server</i>, located inside the
> `Signaling` directory, on a server with at least one port exposed to the internet (for example, VPS).
> The purpose of this server is to coordinate the NAT Hollowing porcess between the two peers. Currently, the code of this
> signaling server is basically a POC, and therefore not stable and scalable. It can easily be replaced by another signaling server,
> as it's protocol will be described later.
> 
![image](https://i.imgur.com/1RH4oua.png)

