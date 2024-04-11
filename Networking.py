from Packets.PacketHandler import Clientbound
from Packets.PacketMap import GameState
from Util import enforce_annotations

import socket

class Networking:
    def __init__(self):
        self.connected_clients = 0
        self.clients = {}

    #TODO: maybe add annotation for packets
    @enforce_annotations
    def broadcast(self, packet, gamestate: GameState):
        for client in self.clients:
            Clientbound(client).send_encrypted(packet, gamestate, self.get_encryptor(client))

    @enforce_annotations
    def send_to_others(self, packet, sender: socket.socket, gamestate: GameState):
        for client in self.clients:
            if client != sender:
                Clientbound(client).send_encrypted(packet, gamestate, self.get_encryptor(client))

    @enforce_annotations
    def add_encryptor(self, socket: socket.socket, encryptor):
        self.clients[socket] = encryptor

    @enforce_annotations
    def get_encryptor(self, socket: socket.socket):
        return self.clients[socket]

    @enforce_annotations
    def remove_encryptor(self, socket: socket.socket):
        self.clients.pop(socket)

    @enforce_annotations
    def add_client(self, socket: socket.socket):
        self.connected_clients += 1
        self.clients[socket] = "encryptor"
        return self.connected_clients

    @enforce_annotations
    def remove_client(self, socket: socket.socket):
        self.connected_clients -= 1
        if socket in self.clients:
            self.clients.pop(socket)
        else:
            print(f"Error: {socket} not in clients")
        return self.connected_clients