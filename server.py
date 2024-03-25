import socket
import struct
import json
import os
import time
import threading

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15

import Packets.PacketUtil
from Packets.Serverbound.StatusRequest import StatusRequest
from Packets.Serverbound.PingRequest import PingRequest
from Packets.Serverbound.LoginStart import LoginStart
from Packets.Serverbound.Handshake import Handshake
from Packets.Serverbound.EncryptionResponse import EncryptionResponse
from Packets.Serverbound.LoginAcknowledged import LoginAcknowledged
from Packets.Serverbound.ServerboundPluginMessage import ServerboundPluginMessage

from Packets.Clientbound.PingResponse import PingResponse
from Packets.Clientbound.StatusResponse import StatusResponse
from Packets.Clientbound.EncryptionRequest import EncryptionRequest
from Packets.Clientbound.LoginSuccess import LoginSuccess

from Packets.PacketHandler import Clientbound, Serverbound
from Packets.PacketUtil import unpack_varint, unpack_encrypted_varint, pack_varint, unpack_varint_bytes
from Packets.ServerData import ServerData

from Encryption import Encryption

def main():
    # Define the port to listen on
    PORT = 25565
    HOST = 'localhost'

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen(5)

    print("Listening on port", PORT)

    next_state = 0

    def get_packet(socket):
        packet_length = unpack_varint(socket)
        packet_id = unpack_varint(socket)
        return serverbound.receive(gamestate, packet_id)

    def get_encrypted_packet(socket, decryptor):
        packet_length = unpack_encrypted_varint(socket)
        packet_id = unpack_encrypted_varint(socket)
        return serverbound.receive(gamestate, packet_id)

    while True:
        client_socket, address = server_socket.accept()

        clientbound = Clientbound(client_socket)
        serverbound = Serverbound(client_socket)

        gamestate = "HANDSHAKE"

        print("Connection from", address)

        if gamestate == "HANDSHAKE":
            packet = get_packet(client_socket)

            if isinstance(packet, Handshake):
                if packet.get("next_state") == 1:
                    gamestate = "STATUS"
                elif packet.get("next_state") == 2:
                    gamestate = "LOGIN"

        if gamestate == "STATUS":
            packet = get_packet(client_socket)

            if isinstance(packet, StatusRequest):
                sample = [
                    {"name": "BlufferFish", "id": "d552a0a7-b211-47c1-9396-5f39dcfedc73"},
                    {"name": "Tuinboon", "id": "d552a0a7-b211-47c1-9396-5f39dcfedc73"}
                ]

                server_data = ServerData(
                    "BlufferFish 1.20.4",
                    765,
                    5,
                    2,
                    sample,
                    "\u00A73Bluffer\u00A7eFish",
                    "icon.png",
                    True,
                    True
                )

                SLP_packet = StatusResponse(server_data.get_data())

                clientbound.send(SLP_packet)


            packet = get_packet(client_socket)

            if isinstance(packet, PingRequest):
                ping_response = PingResponse(packet.get("time"))
                clientbound.send(ping_response)
                print("Sent ping packet")

        if gamestate == "LOGIN":
            packet = get_packet(client_socket)

            if isinstance(packet, LoginStart):
                name = packet.get("name")
                uuid_bytes = packet.get("uuid_bytes")

            do_encryption = True

            if do_encryption:

                encryption = Encryption()
                encryption.gen_keys()

                server_id = ""

                private_key = encryption.get_private_key()

                public_key_der = encryption.get_public_key()

                verify_token = os.urandom(4)

                encryption_request = EncryptionRequest(server_id, public_key_der, verify_token)

                clientbound.send(encryption_request)


                print("Sent encryption request")


                packet = get_packet(client_socket)

                if isinstance(packet, EncryptionResponse):
                    shared_secret = packet.get("shared_secret")
                    verif_token = packet.get("verify_token")

                    shared_secret = private_key.decrypt(shared_secret, PKCS1v15())

                    if private_key.decrypt(verif_token, PKCS1v15()) == verify_token:
                        print("Verification successful")

                        encryption.create_cipher(shared_secret)
                        cipher = encryption.get_cipher()

                        #global encryptor

                        encryptor = cipher.encryptor()
                        decryptor = cipher.decryptor()

                        Packets.PacketUtil.decryptor = decryptor

                        login_success = LoginSuccess(uuid_bytes, name, b'')

                        clientbound.send_encrypted(login_success, encryptor)

                print("Sent login success")

                #LOGIN ACKNOWLEDGEMENT
                packet = get_encrypted_packet(client_socket, decryptor)
                if isinstance(packet, LoginAcknowledged):
                    gamestate = "CONFIGURATION"
                    print("Login Acknowledged")


        if gamestate == "CONFIGURATION":
            if True:
                packet = get_encrypted_packet(client_socket, decryptor)

                if isinstance(packet, ServerboundPluginMessage):
                    print("Plugin Message")

                #print(decryptor.update(client_socket.recv(1024))) #a #plugin channels
                #print(decryptor.update(client_socket.recv(1024))) #a # client info

                #weird ahh registry data

                registry_data = open("registry_info.packet", "rb").read()

                packet = b'\x05' + registry_data

                packet_length = pack_varint(len(packet))

                client_socket.send(encryptor.update(packet_length + packet))

                #configuration finish

                packet = b'\x02'

                packet_length = b'\x01'

                client_socket.send(encryptor.update(packet_length + packet)) #to client
                #print(decryptor.update(client_socket.recv(1024))) #a # to server

                #Play packet
                entity_id = b'\x00\x00\x00\x01'
                is_hardcore = b'\x00'
                dimensions = b'' #pack_varint(len('minecraft:overworld')) + 'minecraft:overworld'.encode('utf-8')
                dimensions_amount = pack_varint(0)
                max_players = pack_varint(5)
                view_distance = pack_varint(12)
                sim_distance = pack_varint(6)
                reduced_debug_info = b'\x00'
                respawn_screen = b'\x00'
                limited_crafting = b'\x00'
                dimension = pack_varint(len('minecraft:overworld')) + "minecraft:overworld".encode('utf-8')
                dimension_name = pack_varint(len('minecraft:overworld')) + "minecraft:overworld".encode('utf-8')
                seed = 123456
                hashed_seed = struct.pack('>q', seed)
                gamemode = b'\x01'
                previous_gamemode = struct.pack('b', -1)
                is_debug = b'\x00'
                is_flat = b'\x01'
                has_death_location = b'\x00'
                portal_cooldown = b'\x00'


                packet = b'\x29' + entity_id + is_hardcore + dimensions_amount + dimensions + max_players + view_distance + sim_distance + reduced_debug_info + respawn_screen + limited_crafting + dimension + dimension_name + hashed_seed + gamemode + previous_gamemode + is_debug + is_flat + has_death_location + portal_cooldown

                packet_length = pack_varint(len(packet))

                client_socket.send(encryptor.update(packet_length + packet))



                print("Login Success")

                #Sync player pos
                double_x = struct.pack('d', 10)
                double_y = struct.pack('d', 100)
                double_z = struct.pack('d', 10)

                float_yaw = struct.pack('f', 0)
                float_pitch = struct.pack('f', 0)

                flags = b'\x00'

                tp_id = pack_varint(123)

                packet = b'\x3E' + double_x + double_y + double_z + float_yaw + float_pitch + flags + tp_id

                packet_length = pack_varint(len(packet))

                client_socket.send(encryptor.update(packet_length + packet))



                #Set default spawn pos

                def encode_coordinates(x, z, y):
                    # Ensure values are within range
                    x &= 0x3FFFFFF  # 26 bits mask
                    z &= 0x3FFFFFF  # 26 bits mask
                    y &= 0xFFF      # 12 bits mask

                    # Combine the values into a single 64-bit integer
                    encoded_value = (x << 38) | (z << 12) | y

                    # If the highest bit of each coordinate is set (indicating negative value), convert to two's complement
                    if x & 0x2000000:
                        x -= 0x4000000
                    if z & 0x2000000:
                        z -= 0x4000000
                    if y & 0x800:
                        y -= 0x1000

                    return encoded_value

                encoded_value = encode_coordinates(10, 10, 100)

                encoded_bytes = struct.pack('>Q', encoded_value)

                packet = b'\x54' + encoded_bytes + struct.pack('f', 0)

                packet_length = pack_varint(len(packet))

                client_socket.send(encryptor.update(packet_length + packet))


                #Game event packet

                packet = b'\x20' + struct.pack('>B', 13) + struct.pack('f', 0)
                packet_length = pack_varint(len(packet))

                client_socket.send(encryptor.update(packet_length + packet))



                #Center chunk

                chunk_x = 0
                chunk_z = 0

                packet = b'\x52' + pack_varint(chunk_x) + pack_varint(chunk_z)

                packet_length = pack_varint(len(packet))

                client_socket.send(encryptor.update(packet_length + packet))



                #Chunk Data and Update Light

                data = b''
                data_length = pack_varint(len(data))

                block_entities = b''
                block_entities_length = pack_varint(len(block_entities))

                stupid_bitsets = b'\x01\x00\x00\x00\x00\x00\x00\x00\x00'

                packet = (b'\x25' + #Packet ID
                          b'\x00\x00\x00\x00' + # Chunk X
                          b'\x00\x00\x00\x00' + # Chunk Z
                          b'\x0A' + #Heightmaps
                          b'\x00' +
                          data_length +
                          data +
                          block_entities_length +
                          block_entities +
                          stupid_bitsets +
                          stupid_bitsets +
                          stupid_bitsets +
                          stupid_bitsets +
                          data_length +
                          data +
                          data_length +
                          data
                          )

                packet_length = pack_varint(len(packet))

                client_socket.send(encryptor.update(packet_length + packet))



                #tp confirm
                #print(decryptor.update(client_socket.recv(1024))) #a


                def keepAlive():
                    while True:
                        time.sleep(29)

                        packet = b'\x24' + struct.pack('>q', 12345678)

                        packet_length = pack_varint(len(packet))

                        client_socket.send(encryptor.update(packet_length + packet))

                threading.Thread(target=keepAlive).start()


                print('crazy?')



            next_state = 0


        #client_socket.close()

if __name__ == "__main__":
    main()