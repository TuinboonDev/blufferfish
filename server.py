import socket
import struct
import json
import os
import time
import threading
import uuid
import requests
import sys
sys.dont_write_bytecode = True

from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from hashlib import sha1

import Packets.PacketUtil

from Packets.Serverbound.StatusRequest import StatusRequest
from Packets.Serverbound.PingRequest import PingRequest
from Packets.Serverbound.LoginStart import LoginStart
from Packets.Serverbound.Handshake import Handshake
from Packets.Serverbound.EncryptionResponse import EncryptionResponse
from Packets.Serverbound.LoginAcknowledged import LoginAcknowledged
from Packets.Serverbound.ServerboundPluginMessage import ServerboundPluginMessage
from Packets.Serverbound.AcknowledgeFinishConfiguration import AcknowledgeFinishConfiguration
from Packets.Serverbound.ConfirmTeleportation import ConfirmTeleportation
from Packets.Serverbound.ClientInformation import ClientInformation
from Packets.Serverbound.SetPlayerPosition import SetPlayerPosition
from Packets.Serverbound.SetPlayerPositionRotation import SetPlayerPositionRotation
from Packets.Serverbound.SetPlayerRotation import SetPlayerRotation

from Packets.Clientbound.PingResponse import PingResponse
from Packets.Clientbound.StatusResponse import StatusResponse
from Packets.Clientbound.EncryptionRequest import EncryptionRequest
from Packets.Clientbound.LoginSuccess import LoginSuccess
from Packets.Clientbound.RegistryData import RegistryData
from Packets.Clientbound.ConfigurationFinish import ConfigurationFinish
from Packets.Clientbound.LoginPlay import LoginPlay
from Packets.Clientbound.SynchronizePlayerPosition import SynchronizePlayerPosition
from Packets.Clientbound.SetDefaultSpawnPosition import SetDefaultSpawnPosition
from Packets.Clientbound.SetCenterChunk import SetCenterChunk
from Packets.Clientbound.ChunkDataUpdateLight import ChunkDataUpdateLight
from Packets.Clientbound.GameEvent import GameEvent
from Packets.Clientbound.KeepAlive import KeepAlive
from Packets.Clientbound.OpenBook import OpenBook
from Packets.Clientbound.DisplayObjective import DisplayObjective
from Packets.Clientbound.SetEntityMetadata import SetEntityMetadata
from Packets.Clientbound.PlayerInfoUpdate import PlayerInfoUpdate
from Packets.Clientbound.SpawnEntity import SpawnEntity
from Packets.Clientbound.UpdateEntityPosition import UpdateEntityPosition
from Packets.Clientbound.SetHeldItem import SetHeldItem
from Packets.Clientbound.UpdateEntityPositionRotation import UpdateEntityPositionRotation
from Packets.Clientbound.UpdateEntityRotation import UpdateEntityRotation

from Packets.PacketHandler import Clientbound, Serverbound
from Packets.PacketUtil import unpack_varint, unpack_encrypted_varint, pack_varint, unpack_varint_bytes, decrypt_byte
from Packets.ServerData import ServerData
from Packets.PacketMap import set_gamestate, get_gamestate

from Encryption import Encryption
from Networking import Networking
from Handlers.GeneralPlayerHandler import GeneralPlayerHandler

def main():
    # Define the port to listen on
    PORT = 25565
    HOST = "localhost"

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen(5)

    print("Listening on port", PORT)

    def get_packet(serverbound, socket):
        packet_length, byte_length = unpack_varint(socket)

        packet_id, byte_length = unpack_varint(socket)
        packet_length -= byte_length
        return serverbound.receive(packet_length, packet_id)

    def get_encrypted_packet(serverbound, socket):
        packet_length, byte_length = unpack_encrypted_varint(socket)

        packet_id, byte_length = unpack_encrypted_varint(socket)
        packet_length -= byte_length
        return serverbound.receive(packet_length, packet_id)

    def handle(client_socket: socket.socket, networking: Networking):
        clientbound = Clientbound(client_socket)
        serverbound = Serverbound(client_socket)

        set_gamestate("HANDSHAKE")

        print("Connection from", address)

        if get_gamestate() == "HANDSHAKE":
            packet = get_packet(serverbound, client_socket)

            if isinstance(packet, Handshake):
                if packet.get("next_state") == 1:
                    set_gamestate("STATUS")
                elif packet.get("next_state") == 2:
                    set_gamestate("LOGIN")

        if get_gamestate() == "STATUS":
            packet = get_packet(serverbound, client_socket)

            if isinstance(packet, StatusRequest):
                sample = [
                    {"name": "BlufferFish", "id": "d552a0a7-b211-47c1-9396-5f39dcfedc73"},
                    {"name": "Tuinboon", "id": "d552a0a7-b211-47c1-9396-5f39dcfedc73"}
                ]

                server_data = ServerData(
                    "BlufferFish 1.20.4",
                    765,
                    5,
                    -5,
                    sample,
                    "\u00A73Bluffer\u00A7eFish",
                    "icon.png",
                    True,
                    True
                )

                SLP_packet = StatusResponse(server_data.get_data())

                clientbound.send(SLP_packet)


            packet = get_packet(serverbound, client_socket)

            if isinstance(packet, PingRequest):
                ping_response = PingResponse(packet.get("time"))
                clientbound.send(ping_response)
                print("Sent ping packet")

        if get_gamestate() == "LOGIN":
            packet = get_packet(serverbound, client_socket)

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


                packet = get_packet(serverbound, client_socket)

                if isinstance(packet, EncryptionResponse):
                    shared_secret = packet.get("shared_secret")
                    verif_token = packet.get("verify_token")

                    shared_secret = private_key.decrypt(shared_secret, PKCS1v15())

                    verification_hash = sha1()

                    verification_hash.update(server_id.encode("utf-8"))
                    verification_hash.update(shared_secret)
                    verification_hash.update(public_key_der)

                    number_representation = int.from_bytes(verification_hash.digest(), byteorder="big", signed=True)
                    hash = format(number_representation, "x")

                    session_auth = requests.get(f"https://sessionserver.mojang.com/session/minecraft/hasJoined?username={name}&serverId={hash}")
                    session_json = session_auth.json()
                    print(session_json)
                    #TODO: Use retrieved data to verify the player

                    print(hash)

                    if private_key.decrypt(verif_token, PKCS1v15()) == verify_token:
                        print("Verification successful")

                        encryption.create_cipher(shared_secret)
                        cipher = encryption.get_cipher()

                        #global encryptor

                        encryptor = cipher.encryptor()
                        decryptor = cipher.decryptor()

                        networking.add_encryptor(client_socket, encryptor)

                        Packets.PacketUtil.decryptor = decryptor

                        login_success = LoginSuccess(uuid_bytes, name, b"")

                        clientbound.send_encrypted(login_success, encryptor)

                print("Sent login success")

                #LOGIN ACKNOWLEDGEMENT
                packet = get_encrypted_packet(serverbound, client_socket)
                if isinstance(packet, LoginAcknowledged):
                    set_gamestate("CONFIGURATION")
                    print("Login Acknowledged")

        if get_gamestate() == "CONFIGURATION":
            packet = get_encrypted_packet(serverbound, client_socket)

            if isinstance(packet, ServerboundPluginMessage):
                #print(packet.get("identifier"))
                #print(packet.get("data"))
                print("Plugin Message")

            packet = get_encrypted_packet(serverbound, client_socket)

            if isinstance(packet, ClientInformation):
                skin_parts = packet.get("displayed_skin_parts")
                general_player_handler.add_player(name, uuid_bytes, session_json["properties"], skin_parts, client_socket)
                print("Client info")

            # Registry Data

            registry_data = RegistryData()

            clientbound.send_encrypted(registry_data, encryptor)

            # configuration finish

            configfinish = ConfigurationFinish()

            clientbound.send_encrypted(configfinish, encryptor)

            packet = get_encrypted_packet(serverbound, client_socket)

            if isinstance(packet, AcknowledgeFinishConfiguration):
                set_gamestate("PLAY")
                print("Configuration Finished")

        if get_gamestate() == "PLAY":
            entity_id = general_player_handler.get_entity_id(uuid_bytes)


            login_play = LoginPlay(
                entity_id,
                False,
                b"",
                5,
                12,
                6,
                False,
                True,
                False,
                "minecraft:overworld",
                "minecraft:overworld",
                123456,
                "creative",
                None,
                False,
                True,
                False,
                None,
                None,
                0
            )

            clientbound.send_encrypted(login_play, encryptor)

            print("Login Success")

            set_held_item = SetHeldItem(b"\x00")

            clientbound.send_encrypted(set_held_item, encryptor)

            # ----

            teleport_id = 123

            sync_player_pos = SynchronizePlayerPosition(8,320,8, 0, 0, b"\x00", teleport_id)

            clientbound.send_encrypted(sync_player_pos, encryptor)

            # Set default spawn pos

            set_default_spawn_pos = SetDefaultSpawnPosition(8, 320, 8, 0)

            clientbound.send_encrypted(set_default_spawn_pos, encryptor)

            # Game event packet

            game_event = GameEvent(13, 0)

            clientbound.send_encrypted(game_event, encryptor)

            # Center chunk

            set_center_chunk = SetCenterChunk(0, 0)

            clientbound.send_encrypted(set_center_chunk, encryptor)

            # Chunk Data and Update Light

            chunk_data_update_light = ChunkDataUpdateLight(0, 0, b"", b"")
            clientbound.send_encrypted(chunk_data_update_light, encryptor)

            # tp confirm
            packet = get_encrypted_packet(serverbound, client_socket)

            if isinstance(packet, ConfirmTeleportation):
                if packet.get("teleport_id") == teleport_id:
                    print("Teleportation confirmed")

            def keepAlive():
                while True:
                    keep_alive = KeepAlive(123)

                    clientbound.send_encrypted(keep_alive, encryptor)
                    time.sleep(29)

            threading.Thread(target=keepAlive).start()

            all_players = general_player_handler.get_online_players()

            for player in all_players:
                add_player = PlayerInfoUpdate([0x01, 0x08], [{"uuid": player["uuid"], "name": player["name"], "show": True}],
                                              {"name": player["properties"][0]["name"],
                                               "value": player["properties"][0]["value"],
                                               "is_signed": True,
                                               "signature": player["properties"][0]["signature"]})


                networking.broadcast(add_player)

            #TODO: change this so it doesn't keep sending to every client

            #--------------------------------------------

            other_players = general_player_handler.get_all_other_players(name)

            for player in other_players:
                spawn_entity = SpawnEntity(player["entity_id"], player["uuid"], 124, 8, 320, 8, b"\x00", b"\x00", b"\x00", 0, 0, 0, 0)

                clientbound.send_encrypted(spawn_entity, encryptor)

            #--------------------------------------------

            # player_count = general_player_handler.get_player_count()

            # if player_count - 1 > 0:
            #     for player in all_players:
            #         if player["name"] == name:
            #             spawn_entity = SpawnEntity(player["entity_id"], player["uuid"], 124, 8, 320, 8, b"\x00", b"\x00", b"\x00", 0, 0, 0, 0)
            #             networking.send_to_others(spawn_entity, client_socket)




            for player in all_players:
                set_entity_metadata = SetEntityMetadata(player["entity_id"], 17, 0, player["skin_parts"])

                networking.broadcast(set_entity_metadata)

            def keepListening():
                prevX = 8
                prevY = 320
                prevZ = 8
                while True:
                    #general_player_handler.get_online_players()[0]["socket"]



                    packet = get_encrypted_packet(serverbound, client_socket)
                    if isinstance(packet, SetPlayerPosition) or isinstance(packet, SetPlayerPositionRotation):
                        on_ground = packet.get("on_ground")
                        #print(prevX, prevY, prevZ)
                        currentX = struct.unpack(">d", packet.get("x"))[0]
                        currentY = struct.unpack(">d", packet.get("y"))[0]
                        currentZ = struct.unpack(">d", packet.get("z"))[0]

                        delta_x = int(currentX * 32 - prevX * 32) * 128
                        delta_y = int(currentY * 32 - prevY * 32) * 128
                        delta_z = int(currentZ * 32 - prevZ * 32) * 128

                        #print(delta_x, delta_y, delta_z)

                        update_entity_position = UpdateEntityPosition(entity_id, delta_x, delta_y, delta_z, on_ground)

                        networking.broadcast(update_entity_position)

                        prevX = currentX
                        prevY = currentY
                        prevZ = currentZ
                    """
                    elif isinstance(packet, SetPlayerPositionRotation):
                        on_ground = packet.get("on_ground")
                        currentX = struct.unpack(">d", packet.get("x"))[0]
                        currentY = struct.unpack(">d", packet.get("y"))[0]
                        currentZ = struct.unpack(">d", packet.get("z"))[0]
                        yaw = packet.get("yaw")
                        pitch = packet.get("pitch")

                        yaw = struct.unpack(">f", yaw)[0]
                        pitch = struct.unpack(">f", pitch)[0]

                        yaw = int((yaw / 360.0) * 256.0) #convert
                        pitch = int((pitch / 360.0) * 256.0) #convert

                        yaw = struct.pack("B", yaw)
                        pitch = struct.pack("B", pitch)

                        print(yaw, pitch, on_ground)

                        delta_x = int(currentX * 32 - prevX * 32) * 128
                        delta_y = int(currentY * 32 - prevY * 32) * 128
                        delta_z = int(currentZ * 32 - prevZ * 32) * 128

                        update_entity_position_rotation = UpdateEntityPositionRotation(entity_id, delta_x, delta_y, delta_z, yaw, pitch, on_ground)

                        networking.broadcast(update_entity_position_rotation)

                        prevX = currentX
                        prevY = currentY
                        prevZ = currentZ
                    
                    elif isinstance(packet, SetPlayerRotation):
                        on_ground = packet.get("on_ground")
                        yaw = packet.get("yaw")
                        pitch = packet.get("pitch")

                        yaw = struct.unpack(">f", yaw)[0]
                        pitch = struct.unpack(">f", pitch)[0]

                        yaw = int((yaw / 360.0) * 256.0) #convert
                        pitch = int((pitch / 360.0) * 256.0) #convert

                        yaw = struct.pack("B", yaw)
                        pitch = struct.pack("B", pitch)

                        update_entity_rotation = UpdateEntityRotation(entity_id, yaw, pitch)

                        networking.broadcast(update_entity_rotation)
                    """


            threading.Thread(target=keepListening).start()

            print("crazy?")
            print("i was crazy once")



    networking = Networking()

    general_player_handler = GeneralPlayerHandler()

    entity_id = 0

    while True:
        client_socket, address = server_socket.accept()

        networking.add_client(client_socket)

        new_connection = threading.Thread(target=handle, args=(client_socket, networking))
        new_connection.start()

        entity_id += 1


if __name__ == "__main__":
    main()