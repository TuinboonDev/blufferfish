import sys
sys.dont_write_bytecode = True
import socket
import struct
import os
import time
import threading
import requests

from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from hashlib import sha1

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
from Packets.Serverbound.PlayerSession import PlayerSession
from Packets.Serverbound.SwingArm import SwingArm

from Packets.Clientbound.SetHeadRotation import SetHeadRotation
from Packets.Clientbound.EntityAnimation import EntityAnimation
from Packets.Clientbound.PingResponse import PingResponse
from Packets.Clientbound.StatusResponse import StatusResponse
from Packets.Clientbound.EncryptionRequest import EncryptionRequest
from Packets.Clientbound.LoginSuccess import LoginSuccess
from Packets.Clientbound.RegistryData import RegistryData
from Packets.Clientbound.ConfigurationFinish import ConfigurationFinish
from Packets.Clientbound.LoginPlay import LoginPlay
from Packets.Clientbound.SynchronizePlayerPosition import SyncronizePlayerPosition
from Packets.Clientbound.SetDefaultSpawnPosition import SetDefaultSpawnPosition
from Packets.Clientbound.SetCenterChunk import SetCenterChunk
from Packets.Clientbound.ChunkDataUpdateLight import ChunkDataUpdateLight
from Packets.Clientbound.GameEvent import GameEvent
from Packets.Clientbound.KeepAlive import KeepAlive
from Packets.Clientbound.SetEntityMetadata import SetEntityMetadata
from Packets.Clientbound.PlayerInfoUpdate import PlayerInfoUpdate
from Packets.Clientbound.SpawnEntity import SpawnEntity
from Packets.Clientbound.UpdateEntityPosition import UpdateEntityPosition
from Packets.Clientbound.SetHeldItem import SetHeldItem
from Packets.Clientbound.UpdateEntityPositionRotation import UpdateEntityPositionRotation
from Packets.Clientbound.UpdateEntityRotation import UpdateEntityRotation

from Packets.PacketHandler import Clientbound, Serverbound
from Packets.ServerData import ServerData
from Packets.PacketMap import GameState
from Packets.PacketUtil import ByteBuffer, unpack_varint, unpack_encrypted_varint

from Encryption import Encryption
from Networking import Networking
from Handlers.GeneralPlayerHandler import GeneralPlayerHandler

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

    def get_packet(serverbound, socket, gamestate):
        packet_length, byte_length = unpack_varint(socket)

        buf = ByteBuffer(socket.recv(packet_length))

        packet_id, byte_length = buf.unpack_varint()
        return serverbound.receive(buf, packet_id, gamestate, None)

    def get_encrypted_packet(serverbound, socket, gamestate, decryptor):
        packet_length, byte_length = unpack_encrypted_varint(socket, decryptor)

        buf = ByteBuffer(socket.recv(packet_length))

        packet_id, byte_length = buf.unpack_encrypted_varint(decryptor)
        return serverbound.receive(buf, packet_id, gamestate, decryptor)
    
    def handle(client_socket, networking):
        clientbound = Clientbound(client_socket)
        serverbound = Serverbound()

        gamestate = GameState()

        print("Connection from", address)

        if gamestate.get_gamestate() == "HANDSHAKE":
            packet = get_packet(serverbound, client_socket, gamestate)

            if isinstance(packet, Handshake):
                if packet.get("next_state") == 1:
                    gamestate.set_gamestate("STATUS")
                elif packet.get("next_state") == 2:
                    gamestate.set_gamestate("LOGIN")

        if gamestate.get_gamestate() == "STATUS":
            packet = get_packet(serverbound, client_socket, gamestate)

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

                clientbound.send(SLP_packet, gamestate)


            packet = get_packet(serverbound, client_socket, gamestate)

            if isinstance(packet, PingRequest):
                ping_response = PingResponse(packet.get("time"))
                clientbound.send(ping_response, gamestate)
                print("Sent ping packet")

        if gamestate.get_gamestate() == "LOGIN":
            packet = get_packet(serverbound, client_socket, gamestate)

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

                clientbound.send(encryption_request, gamestate)


                print("Sent encryption request")


                packet = get_packet(serverbound, client_socket, gamestate)

                if isinstance(packet, EncryptionResponse):
                    shared_secret = packet.get("shared_secret")
                    verif_token = packet.get("verify_token")

                    shared_secret = private_key.decrypt(shared_secret, PKCS1v15())

                    verification_hash = sha1()

                    verification_hash.update(server_id.encode('utf-8'))
                    verification_hash.update(shared_secret)
                    verification_hash.update(public_key_der)

                    number_representation = int.from_bytes(verification_hash.digest(), byteorder='big', signed=True)
                    hash = format(number_representation, 'x')

                    session_auth = requests.get(f"https://sessionserver.mojang.com/session/minecraft/hasJoined?username={name}&serverId={hash}")
                    session_json = session_auth.json()
                    #TODO: Use retrieved data to verify the player

                    if private_key.decrypt(verif_token, PKCS1v15()) == verify_token:
                        print("Verification successful")

                        encryption.create_cipher(shared_secret)
                        cipher = encryption.get_cipher()

                        #global gamestate, encryptor

                        encryptor = cipher.encryptor()
                        decryptor = cipher.decryptor()

                        networking.add_encryptor(client_socket, encryptor)

                        login_success = LoginSuccess(uuid_bytes, name, b'')

                        clientbound.send_encrypted(login_success, gamestate, encryptor)

                print("Sent login success")

                #LOGIN ACKNOWLEDGEMENT
                packet = get_encrypted_packet(serverbound, client_socket, gamestate, decryptor)
                if isinstance(packet, LoginAcknowledged):
                    gamestate.set_gamestate("CONFIGURATION")
                    print("Login Acknowledged")

        if gamestate.get_gamestate() == "CONFIGURATION":
            packet = get_encrypted_packet(serverbound, client_socket, gamestate, decryptor)

            if isinstance(packet, ServerboundPluginMessage):
                print("Plugin Message")

            packet = get_encrypted_packet(serverbound, client_socket, gamestate, decryptor)

            if isinstance(packet, ClientInformation):
                skin_parts = packet.get("displayed_skin_parts")
                print("Client info")

            # Registry Data

            registry_data = RegistryData()

            clientbound.send_encrypted(registry_data, gamestate, encryptor)

            # configuration finish

            configfinish = ConfigurationFinish()

            clientbound.send_encrypted(configfinish, gamestate, encryptor)

            packet = get_encrypted_packet(serverbound, client_socket, gamestate, decryptor)

            if isinstance(packet, AcknowledgeFinishConfiguration):
                gamestate.set_gamestate("PLAY")
                print("Configuration Finished")

        if gamestate.get_gamestate() == "PLAY":
            general_player_handler.add_player(name, uuid_bytes, session_json["properties"], skin_parts, client_socket)
            entity_id = general_player_handler.get_entity_id(uuid_bytes)


            login_play = LoginPlay(
                entity_id,
                False,
                b'',
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

            clientbound.send_encrypted(login_play, gamestate, encryptor)

            print("Login Success")

            set_held_item = SetHeldItem(b'\x00')

            clientbound.send_encrypted(set_held_item, gamestate, encryptor)

            # ----

            teleport_id = 123

            sync_player_pos = SyncronizePlayerPosition(8,320,8, 0, 0, b'\x00', teleport_id)

            clientbound.send_encrypted(sync_player_pos, gamestate, encryptor)

            # Set default spawn pos

            set_default_spawn_pos = SetDefaultSpawnPosition(8, 320, 8, 0)

            clientbound.send_encrypted(set_default_spawn_pos, gamestate, encryptor)

            # Game event packet

            game_event = GameEvent(13, 0)

            clientbound.send_encrypted(game_event, gamestate, encryptor)

            # Center chunk

            set_center_chunk = SetCenterChunk(0, 0)

            clientbound.send_encrypted(set_center_chunk, gamestate, encryptor)

            # Chunk Data and Update Light

            chunk_data_update_light = ChunkDataUpdateLight(0, 0, b'', b'')
            clientbound.send_encrypted(chunk_data_update_light, gamestate, encryptor)

            # tp confirm
            packet = get_encrypted_packet(serverbound, client_socket, gamestate, decryptor)

            if isinstance(packet, ConfirmTeleportation):
                if packet.get("teleport_id") == teleport_id:
                    print("Teleportation confirmed")

            def keepAlive():
                while True:
                    keep_alive = KeepAlive(123)

                    clientbound.send_encrypted(keep_alive, gamestate, encryptor)
                    time.sleep(29)

            threading.Thread(target=keepAlive).start()

            all_players = general_player_handler.get_online_players()

            for player in all_players:
                add_player = PlayerInfoUpdate([0x01, 0x08], [{"uuid": player["uuid"], "name": player["name"], "show": True}],
                                              {"name": player["properties"][0]["name"],
                                               "value": player["properties"][0]["value"],
                                               "is_signed": True,
                                               "signature": player["properties"][0]["signature"]})


                networking.broadcast(add_player, gamestate)

            #TODO: change this so it doesnt keep sending to every client

            #--------------------------------------------

            other_players = general_player_handler.get_all_other_players(name)

            for player in other_players:
                spawn_entity = SpawnEntity(player["entity_id"], player["uuid"], 124, 8, 320, 8, b'\x00', b'\x00', b'\x00', 0, 0, 0, 0)

                clientbound.send_encrypted(spawn_entity, gamestate, encryptor)

            #--------------------------------------------

            player_count = general_player_handler.get_player_count()

            if player_count - 1 > 0:
                for player in all_players:
                    if player["name"] == name:
                        spawn_entity = SpawnEntity(player["entity_id"], player["uuid"], 124, 8, 320, 8, b'\x00', b'\x00', b'\x00', 0, 0, 0, 0)
                        networking.send_to_others(spawn_entity, client_socket, gamestate)




            for player in all_players:
                set_entity_metadata = SetEntityMetadata(player["entity_id"], 17, 0, player["skin_parts"])

                networking.broadcast(set_entity_metadata, gamestate)

            def keepListening():
                prevX = 8
                prevY = 320
                prevZ = 8
                while True:
                    #general_player_handler.get_online_players()[0]["socket"]

                    packet = get_encrypted_packet(serverbound, client_socket, gamestate, decryptor)
                    if isinstance(packet, PlayerSession):
                        print("Player Session")

                    elif isinstance(packet, SetPlayerPosition):
                        on_ground = packet.get("on_ground")
                        currentX = struct.unpack('>d', packet.get("x"))[0]
                        currentY = struct.unpack('>d', packet.get("y"))[0]
                        currentZ = struct.unpack('>d', packet.get("z"))[0]

                        delta_x = int((currentX * 32 - prevX * 32) * 128)
                        delta_y = int((currentY * 32 - prevY * 32) * 128)
                        delta_z = int((currentZ * 32 - prevZ * 32) * 128)

                        update_entity_position = UpdateEntityPosition(entity_id, delta_x, delta_y, delta_z, on_ground)

                        networking.send_to_others(update_entity_position, client_socket, gamestate)

                        prevX = currentX
                        prevY = currentY
                        prevZ = currentZ
                    elif isinstance(packet, SetPlayerPositionRotation):
                        on_ground = packet.get("on_ground")
                        currentX = struct.unpack('>d', packet.get("x"))[0]
                        currentY = struct.unpack('>d', packet.get("y"))[0]
                        currentZ = struct.unpack('>d', packet.get("z"))[0]
                        yaw = packet.get("yaw")
                        pitch = packet.get("pitch")

                        yaw = struct.unpack('>f', yaw)[0]
                        pitch = struct.unpack('>f', pitch)[0]

                        print(yaw, pitch)

                        yaw = int((yaw / 360.0) * 256.0) & 0xff #convert
                        pitch = int((pitch / 360.0) * 256.0) & 0xff #convert

                        yaw = struct.pack("B", yaw)
                        pitch = struct.pack("B", pitch)

                        print(yaw, pitch)

                        delta_x = int((currentX * 32 - prevX * 32) * 128)
                        delta_y = int((currentY * 32 - prevY * 32) * 128)
                        delta_z = int((currentZ * 32 - prevZ * 32) * 128)

                        update_entity_position_rotation = UpdateEntityPositionRotation(entity_id, delta_x, delta_y, delta_z, yaw, pitch, on_ground)

                        networking.send_to_others(update_entity_position_rotation, client_socket, gamestate)

                        set_head_rotation = SetHeadRotation(entity_id, yaw)

                        networking.send_to_others(set_head_rotation, client_socket, gamestate)

                        prevX = currentX
                        prevY = currentY
                        prevZ = currentZ

                    elif isinstance(packet, SetPlayerRotation):
                        on_ground = packet.get("on_ground")
                        yaw = packet.get("yaw")
                        pitch = packet.get("pitch")

                        yaw = struct.unpack('>f', yaw)[0]
                        pitch = struct.unpack('>f', pitch)[0]

                        yaw = int((yaw / 360.0) * 256.0) & 0xff #convert
                        pitch = int((pitch / 360.0) * 256.0) & 0xff #convert

                        yaw = struct.pack("B", yaw)
                        pitch = struct.pack("B", pitch)

                        update_entity_rotation = UpdateEntityRotation(entity_id, yaw, pitch, on_ground)

                        networking.send_to_others(update_entity_rotation, client_socket, gamestate)

                        set_head_rotation = SetHeadRotation(entity_id, yaw)

                        networking.send_to_others(set_head_rotation, client_socket, gamestate)
                    elif isinstance(packet, SwingArm):
                        hand = packet.get("hand")

                        print(hand)

                        if hand == 0:
                            animation = 0

                        elif hand == 1:
                            animation = 3

                        entity_animation = EntityAnimation(entity_id, animation)

                        networking.send_to_others(entity_animation, client_socket, gamestate)




            threading.Thread(target=keepListening).start()

            print('crazy?')



    networking = Networking()

    general_player_handler = GeneralPlayerHandler()

    entity_id = 0

    while True:
        client_socket, address = server_socket.accept()

        test = ''

        networking.add_client(client_socket)

        new_connection = threading.Thread(target=handle, args=(client_socket, networking))
        new_connection.start()

        entity_id += 1
        

if __name__ == "__main__":
    main()