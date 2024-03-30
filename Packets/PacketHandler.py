from Packets.PacketMap import GameStates, get_gamestate
from Packets.PacketUtil import pack_varint
from Packets.PacketMap import GameStates

class Clientbound:
    def __init__(self, socket):
        self.socket = socket

    def __send(self, packet, encryption):
        packet_id_map = {v: k for k, v in GameStates[get_gamestate()]["S2C"].items()}

        packet_class = type(packet)

        try:
            final_packet = pack_varint(packet_id_map.get(packet_class))
        except TypeError as e:
            print(packet)
            print(packet_id_map)
            raise TypeError(f"Packet {packet_class} is not in the PacketMap") from e


        for key in list(packet.__dict__.keys()):
            final_packet += packet.__dict__[key]

        if packet_class.__name__ == "PlayerInfoUpdate":
            print(len(final_packet))
            for x in final_packet:
                print(x)

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

    def receive(self, packet_id):
        packet = GameStates[get_gamestate()]["C2S"][packet_id]().create(self.socket)

        return packet