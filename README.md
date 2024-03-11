# Secret Chat
End to End encrypted and modular chat, with the ability to support a
variety of communications and encryption.

### Supported communication types:
* <b>Client Server Architecture</b> - Regular Client-Server mode, over <i>TCP</i> socket (called just `TCP` in
the code for simpler name) Exists in the program only to show her ability to be modular, and also to test other modules
(currently only encryption-related) without the need to use the more complicated way of communication, UDP Hole punching.
* <b>NAT Hollowing</b> - Peer to Peer Communication over UDP socket. The "Server" Hollow his NAT table,
and then the "client" communicate to him over this "Hole". This communication mode allows peers that are  behind
NAT Tables (like most of the end users) to communicate directly, without the need of middle server, and therefor the most secured.

> [!NOTE]
> Essential details that users should not overlook, even when browsing quickly.