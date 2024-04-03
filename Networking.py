from Packets.PacketHandler import Clientbound

class Networking:
    def __init__(self):
        self.connected_clients = 0
        self.clients = {}

    def broadcast(self, packet):
        for client in self.clients:
            Clientbound(client).send_encrypted(packet, self.get_encryptor(client))

    def send_to_others(self, packet, sender):
        for client in self.clients:
            if client != sender:
                Clientbound(client).send_encrypted(packet, self.get_encryptor(client))

    def add_encryptor(self, socket, encryptor):
        self.clients[socket] = encryptor

    def get_encryptor(self, socket):
        return self.clients[socket]

    def remove_encryptor(self, socket):
        self.clients.pop(socket)

    def add_client(self, socket):
        self.connected_clients += 1
        self.clients[socket] = "encryptor"
        return self.connected_clients

    def remove_client(self, socket):
        self.connected_clients -= 1
        self.clients.pop(socket)
        return self.connected_clients