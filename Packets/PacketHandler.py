from Packets.PacketMap import GameStates
from Packets.PacketUtil import pack_varint

from Packets.Clientbound.LoginSuccess import LoginSuccess

class Clientbound:
    def __init__(self, socket):
        self.socket = socket

    def __send(self, packet, encryption):
        final_packet = b''

        for key in list(packet.__dict__.keys()):
            final_packet += packet.__dict__[key]

        try:
            if encryption is not None:
                self.socket.send(encryption.update(pack_varint(len(final_packet)) + final_packet))
            else:
                self.socket.send(pack_varint(len(final_packet)) + final_packet)
            return True
        except Exception as e:
            print(f"Error sending packet: {e}")
            return False

    def send(self, packet):
        self.__send(packet, None)

    def send_encrypted(self, packet, encryptor):
        self.__send(packet, encryptor)

class Serverbound:
    def __init__(self, socket):
        self.socket = socket

    def receive(self, gamestate, packet_id):
        packet = GameStates[gamestate]["C2S"][packet_id]().create(self.socket)

        return packet