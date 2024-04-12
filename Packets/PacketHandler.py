from Packets.PacketUtil import Pack
from Packets.PacketMap import GameStates, GameState
from Encryption import Encryption

import socket
import sys

Pack = Pack()


class Clientbound:
    def __init__(self, socket: socket.socket):
        self.socket = socket

    def __send(self, packet, gamestate, encryptor):
        print(packet)
        #packet_id_map = {v: k for k, v in GameStates[gamestate.get_gamestate()]["S2C"].items()}
        for p in list(GameStates[gamestate.get_gamestate()]["S2C"].values()):
            if p[0]["class"] == type(packet):
                p.pop(0)
                packet_sequence = p
                break

        final_packet = b''

        for x in range(len(packet.get())):
            method = list(packet_sequence[x].values())[x]
            input = list(packet.__dict__.values())[x]
            print(input)
            print(method)
            print(method(input))
            final_packet += method(input)
            break

        print("\n\n")
        print(final_packet)

        if encryptor is not None:
            self.socket.send(encryptor.update(Pack.pack_varint(len(final_packet)) + final_packet))
        else:
            self.socket.send(Pack.pack_varint(len(final_packet)) + final_packet)

    def send(self, packet, gamestate):
        self.__send(packet, gamestate, None)

    def send_encrypted(self, packet, gamestate, encryptor):
        self.__send(packet, gamestate, encryptor)

class Serverbound:
    def receive(self, bytebuf, packet_id, gamestate, decryptor):
        #Is this if statement reliable?

        game_state = gamestate.get_gamestate()
        if packet_id not in GameStates[game_state]["C2S"]:
            raise ValueError(f"Packet ID {packet_id} is not in the PacketMap")

        packet_data = {"name": GameStates[game_state]["C2S"][packet_id][0]["name"]}

        for payload in GameStates[game_state]["C2S"][packet_id]:
            for key, value in payload.items():
                if list(payload.keys())[0] == "encrypted" or list(payload.keys())[0] == "name":
                    continue
                packet_data[key] = value(bytebuf, decryptor)

        print(packet_data)

        return packet_data