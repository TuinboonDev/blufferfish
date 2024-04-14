from Packets.PacketUtil import Pack
from Packets.PacketMap import GameStates
from Encryption import Encryption

import socket
import sys

Pack = Pack()


class Clientbound:
    def __init__(self, socket: socket.socket):
        self.socket = socket

    def __send(self, packet, gamestate, encryptor):
        gamestate_packets = list(GameStates[gamestate.get_gamestate()]["S2C"].values())

        for gamestate_packet in gamestate_packets:
            packet_name = list(gamestate_packet.keys())[0]
            if packet_name == packet.__class__.__name__:
                packet_sequence = list(gamestate_packet.values())[0]
                break

        for packet_id, packet_data in GameStates[gamestate.get_gamestate()]["S2C"].items():
            if list(packet_data.keys())[0] == packet.__class__.__name__:
                packet_id = packet_id
                break

        #TODO: combine into one for loop

        final_packet = Pack.pack_varint(packet_id)

        for x in range(len(packet.get())):
            try:
                method = list(packet_sequence[x].values())[0]
                input = packet.get()[x]
                final_packet += method(input)
            except Exception as e:
                print("\n")
                print(method)
                print(input)
                print(packet.get())
                print(packet_sequence)


        if encryptor is not None:
            self.socket.send(encryptor.update(Pack.pack_varint(len(final_packet)) + final_packet))
        else:
            self.socket.send(Pack.pack_varint(len(final_packet)) + final_packet)

        if packet.__class__.__name__ == "SynchronizePlayerPosition":
            print(Pack.pack_varint(len(final_packet)) + final_packet)

    def send(self, packet, gamestate):
        self.__send(packet, gamestate, None)

    def send_encrypted(self, packet, gamestate, encryptor):
        self.__send(packet, gamestate, encryptor)

class Serverbound:
    def receive(self, bytebuf, packet_id, gamestate, decryptor):
        game_state = gamestate.get_gamestate()
        print(GameStates)
        if packet_id not in GameStates[game_state]["C2S"]:
            raise ValueError(f"Packet ID {packet_id} is not in the PacketMap")

        packet_name = list(GameStates[game_state]["C2S"][packet_id].keys())[0]

        packet_data = {"packet_name": packet_name}

        for payload in GameStates[game_state]["C2S"][packet_id][packet_name]:
            for key, value in payload.items():
                try:
                    packet_data[key] = value(bytebuf, decryptor)
                except Exception as e:
                    print(key)
                    print("EEEEEEEEE")
                    print(value)
                    print(bytebuf.buffer)
                    print("BBBBBB")
                    raise e

        return packet_data