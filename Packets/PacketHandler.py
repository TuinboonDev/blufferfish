from Packets.PacketUtil import pack_varint
from Packets.PacketMap import GameStates
import sys

class Clientbound:
    def __init__(self, socket):
        self.socket = socket

    def __send(self, packet, gamestate, encryption):
        packet_id_map = {v: k for k, v in GameStates[gamestate.get_gamestate()]["S2C"].items()}

        packet_class = type(packet)

        try:
            final_packet = pack_varint(packet_id_map.get(packet_class))
        except TypeError as e:
            raise TypeError(f"Packet {packet_class} is not in the PacketMap") from e


        for key in list(packet.__dict__.keys()):
            final_packet += packet.__dict__[key]

        if packet_class.__name__ == "SyncronizePlayerPosition" or packet_class.__name__ == "SetDefaultSpawnPosition":
            #print(len(final_packet))
            #for x in final_packet:
            #    print(x)
            #print("\n")
            pass

        try:
            if encryption is not None:
                self.socket.send(encryption.update(pack_varint(len(final_packet)) + final_packet))
            else:
                self.socket.send(pack_varint(len(final_packet)) + final_packet)
            return True
        except ConnectionAbortedError as e:
            print("Client disconnected, shutting down keepalive thread")
            sys.exit()
        except Exception as e:
            print(f"Error while sending packet: {e}")
            return False

    def send(self, packet, gamestate):
        self.__send(packet, gamestate, None)

    def send_encrypted(self, packet, gamestate, encryptor):
        self.__send(packet, gamestate, encryptor)

class Serverbound:
    def receive(self, bytebuf, packet_id, gamestate, decryptor):
        #Is this if statement reliable?

        game_state = gamestate.get_gamestate()
        if game_state not in GameStates or "C2S" not in GameStates[game_state] or packet_id not in GameStates[game_state]["C2S"]:
            #Packets like 0x17 == 23 are not in the PacketMap because the game_state is not in the right state yet
            raise ValueError(f"Packet ID {packet_id} is not in the PacketMap")


        packet = GameStates[game_state]["C2S"][packet_id]().create(bytebuf, decryptor)

        return packet