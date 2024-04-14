import sys
sys.dont_write_bytecode = True
import socket
import struct
import os
import time
import threading
import json
import requests

from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from hashlib import sha1

from Packets.Serverbound.PingRequest import PingRequest
from Packets.Serverbound.StatusRequest import StatusRequest
from Packets.Clientbound.PingResponse import PingResponse
from Packets.Clientbound.StatusResponse import StatusResponse
from Packets.Clientbound.EncryptionRequest import EncryptionRequest
from Packets.Clientbound.LoginSuccess import LoginSuccess
from Packets.Clientbound.RegistryData import RegistryData
from Packets.Clientbound.ConfigurationFinish import ConfigurationFinish
from Packets.Clientbound.SetHeldItem import SetHeldItem
from Packets.Clientbound.LoginPlay import LoginPlay
from Packets.Clientbound.SynchronizePlayerPosition import SynchronizePlayerPosition
from Packets.Clientbound.SetDefaultSpawnPosition import SetDefaultSpawnPosition
from Packets.Clientbound.GameEvent import GameEvent
from Packets.Clientbound.SetCenterChunk import SetCenterChunk
from Packets.Clientbound.UpdateEntityPosition import UpdateEntityPosition
from Packets.Clientbound.UpdateEntityRotation import UpdateEntityRotation
from Packets.Clientbound.KeepAlive import KeepAlive
from Packets.Clientbound.ChunkDataUpdateLight import ChunkDataUpdateLight
from Packets.Clientbound.PlayerInfoUpdate import PlayerInfoUpdate
from Packets.Clientbound.SpawnEntity import SpawnEntity
from Packets.Clientbound.SetEntityMetadata import SetEntityMetadata
from Packets.Clientbound.SetHeadRotation import SetHeadRotation
from Packets.Clientbound.UpdateEntityPositionRotation import UpdateEntityPositionRotation
from Packets.Clientbound.EntityAnimation import EntityAnimation
from Packets.Clientbound.AcknowledgeBlockChange import AcknowledgeBlockChange
from Packets.Clientbound.BlockUpdate import BlockUpdate
from Packets.Clientbound.WorldEvent import WorldEvent

from Packets.Serverbound.Handshake import Handshake

from Packets.PacketHandler import Clientbound, Serverbound
from Packets.ServerData import ServerData
from Packets.PacketMap import GameState
from Packets.PacketUtil import ByteBuffer, Unpack

from Encryption import Encryption
from Networking import Networking
from Handlers.GeneralPlayerHandler import GeneralPlayerHandler
from Exceptions import ClientError
from Util import enforce_annotations

print("""
\u001b[36m ____  __    __  __  ____  ____  ____  ____    \u001b[33;1m____  ____  ___  _   _ 
\u001b[36m(  _ \(  )  (  )(  )( ___)( ___)( ___)(  _ \  \u001b[33;1m( ___)(_  _)/ __)( )_( )
\u001b[36m ) _ < )(__  )(__)(  )__)  )__)  )__)  )   /   \u001b[33;1m)__)  _)(_ \__ \ ) _ ( 
\u001b[36m(____/(____)(______)(__)  (__)  (____)(_)\_)  \u001b[33;1m(__)  (____)(___/(_) (_)
                                                                                            \033[0m""")

Unpack = Unpack()

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

    @enforce_annotations
    def get_packet(serverbound: Serverbound, socket: socket.socket, gamestate: GameState):
        try:
            packet_length = Unpack.unpack_varint(socket)
        except TypeError as e:
            raise e
            ClientError("Client disconnected")
            #networking.remove_client(socket)
            #general_player_handler.remove_player(socket)
            sys.exit()

        buf = ByteBuffer(socket.recv(packet_length))

        packet_id = Unpack.unpack_varint(buf)
        return serverbound.receive(buf, packet_id, gamestate, None)

    @enforce_annotations
    def get_encrypted_packet(serverbound: Serverbound, socket: socket.socket, gamestate: GameState, decryptor):
        try:
            packet_length = Unpack.unpack_encrypted_varint(socket, decryptor)
        except TypeError:
            #TODO: add custom client disconnect error
            ClientError("Client disconnected")
            networking.remove_client(socket)
            general_player_handler.remove_player(socket)
            sys.exit()

        buf = ByteBuffer(socket.recv(packet_length))

        packet_id = Unpack.unpack_encrypted_varint(buf, decryptor)
        return serverbound.receive(buf, packet_id, gamestate, decryptor)

    @enforce_annotations
    def handle(client_socket: socket.socket, networking: Networking):
        clientbound = Clientbound(client_socket)
        serverbound = Serverbound()

        gamestate = GameState()

        print("\u001b[32mConnection from", address, "\u001b[0m")

        if gamestate.get_gamestate() == "HANDSHAKE":
            packet = get_packet(serverbound, client_socket, gamestate)

            if packet.get("packet_name") == "Handshake":
                if packet.get("next_state") == 1:
                    gamestate.set_gamestate("STATUS")
                elif packet.get("next_state") == 2:
                    gamestate.set_gamestate("LOGIN")

        if gamestate.get_gamestate() == "STATUS":
            packet = get_packet(serverbound, client_socket, gamestate)

            if packet.get("packet_name") == "StatusRequest":
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
                    "BlufferFish",#\u00A73Bluffer\u00A7eFish
                    "icon.png",
                    False,
                    True
                )

                SLP_packet = StatusResponse(json.dumps(server_data.get_data()))

                clientbound.send(SLP_packet, gamestate)

            packet = get_packet(serverbound, client_socket, gamestate)

            if packet.get("packet_name") == "PingRequest":
                ping_response = PingResponse(packet.get("time"))
                clientbound.send(ping_response, gamestate)
                print("Sent ping packet")

        if gamestate.get_gamestate() == "LOGIN":
            packet = get_packet(serverbound, client_socket, gamestate)

            if packet.get("packet_name") == "LoginStart":
                name = packet.get("name")
                uuid_bytes = packet.get("uuid")

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

                if packet.get("packet_name") == "EncryptionResponse":
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

                        networking.add_client(client_socket)
                        networking.add_encryptor(client_socket, encryptor)

                        login_success = LoginSuccess(uuid_bytes, name, b'')

                        clientbound.send_encrypted(login_success, gamestate, encryptor)

                print("Sent login success")

                #LOGIN ACKNOWLEDGEMENT
                packet = get_encrypted_packet(serverbound, client_socket, gamestate, decryptor)
                if packet.get("packet_name") == "LoginAcknowledged":
                    gamestate.set_gamestate("CONFIGURATION")
                    print("Login Acknowledged")

        if gamestate.get_gamestate() == "CONFIGURATION":
            packet = get_encrypted_packet(serverbound, client_socket, gamestate, decryptor)

            if packet.get("packet_name") == "ServerboundPluginMessage":
                print("Plugin Message")

            packet = get_encrypted_packet(serverbound, client_socket, gamestate, decryptor)

            if packet.get("packet_name") == "ClientInformation":
                skin_parts = packet.get("displayed_skin_parts")
                print("Client info")

            # Registry Data

            registry_data = RegistryData(open("registry_info.packet", "rb").read())

            clientbound.send_encrypted(registry_data, gamestate, encryptor)

            # configuration finish

            configfinish = ConfigurationFinish()

            clientbound.send_encrypted(configfinish, gamestate, encryptor)

            packet = get_encrypted_packet(serverbound, client_socket, gamestate, decryptor)

            if packet.get("packet_name") == "AcknowledgeFinishConfiguration":
                gamestate.set_gamestate("PLAY")
                print("Configuration Finished")

        if gamestate.get_gamestate() == "PLAY":
            general_player_handler.add_player(name, uuid_bytes, session_json, skin_parts, client_socket)
            entity_id = general_player_handler.get_entity_id(uuid_bytes)


            login_play = LoginPlay(
                entity_id,
                b'\x00',
                b'',
                5,
                12,
                6,
                b'\x00',
                b'\x01',
                b'\x00',
                "minecraft:overworld",
                "minecraft:overworld",
                123456,
                "creative",
                b'\x00',
                b'\x00',
                b'\x01',
                b'\x00',
                0
            )

            clientbound.send_encrypted(login_play, gamestate, encryptor)

            print("Login Success")

            set_held_item = SetHeldItem(b'\x00')

            clientbound.send_encrypted(set_held_item, gamestate, encryptor)

            print("Held item")

            # ----

            position = general_player_handler.get_position(entity_id)
            rotation = general_player_handler.get_rotation(entity_id)

            teleport_id = 123

            sync_player_pos = SynchronizePlayerPosition(position[0], position[1], position[2], rotation[0], rotation[1], b'\x00', teleport_id)

            clientbound.send_encrypted(sync_player_pos, gamestate, encryptor)

            print("Sync player pos")

            # Set default spawn pos

            set_default_spawn_pos = SetDefaultSpawnPosition(position[0], position[1], position[2], rotation[0])

            clientbound.send_encrypted(set_default_spawn_pos, gamestate, encryptor)

            print("Set default spawn pos")

            # Game event packet

            game_event = GameEvent(13, 0)

            clientbound.send_encrypted(game_event, gamestate, encryptor)

            print("Game event")

            # Center chunk

            set_center_chunk = SetCenterChunk(0, 0)

            clientbound.send_encrypted(set_center_chunk, gamestate, encryptor)

            # Chunk Data and Update Light

            width = 20
            height = 20

            center = 0

            start = (width // 2, height // 2)

            x_coord = center - start[0]
            y_coord = center - start[1]

            for x in range(width + 1 if width % 2 == 0 else width):
                for y in range(height + 1 if height % 2 == 0 else height):
                    chunk_data_update_light = ChunkDataUpdateLight(x_coord, y_coord, b'', b'')
                    clientbound.send_encrypted(chunk_data_update_light, gamestate, encryptor)
                    y_coord += 1
                x_coord += 1
                y_coord = center - start[1]

            # tp confirm
            packet = get_encrypted_packet(serverbound, client_socket, gamestate, decryptor)

            if packet.get("packet_name") == "ConfirmTeleportation":
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
                add_player = PlayerInfoUpdate([0x01, 0x08], [{"uuid": player.uuid, "name": player.name, "show": True}],
                                              {"name": player.session["properties"][0]["name"],
                                               "value": player.session["properties"][0]["value"],
                                               "is_signed": True,
                                               "signature": player.session["properties"][0]["signature"]})


                networking.broadcast(add_player, gamestate)

            #TODO: change this so it doesnt keep sending to every client

            #--------------------------------------------

            other_players = general_player_handler.get_all_other_players(name)

            for player in other_players:
                position = general_player_handler.get_position(player.entity_id)
                rotation = general_player_handler.get_rotation(player.entity_id)
                spawn_entity = SpawnEntity(player.entity_id, player.uuid, 124, position[0], position[1], position[2], rotation[0], rotation[1], rotation[1], 0, 0, 0, 0)

                clientbound.send_encrypted(spawn_entity, gamestate, encryptor)

            #--------------------------------------------

            player_count = general_player_handler.get_player_count()

            if player_count - 1 > 0:
                for player in all_players:
                    if player.name == name:
                        position = general_player_handler.get_position(player.entity_id)
                        rotation = general_player_handler.get_rotation(player.entity_id)
                        spawn_entity = SpawnEntity(player.entity_id, player.uuid, 124, position[0], position[1], position[2], rotation[0], rotation[1], rotation[1], 0, 0, 0, 0)
                        networking.send_to_others(spawn_entity, client_socket, gamestate)




            for player in all_players:
                set_entity_metadata = SetEntityMetadata(player.entity_id, [{"index": 17, "value_type": 0, "value": player.skin_parts}])

                networking.broadcast(set_entity_metadata, gamestate)

            def keepListening():
                while True:
                    position = general_player_handler.get_position(entity_id)

                    prevX = position[0]
                    prevY = position[1]
                    prevZ = position[2]

                    packet = get_encrypted_packet(serverbound, client_socket, gamestate, decryptor)
                    if packet.get("packet_name") == "PlayerSession":
                        print("Player Session")

                    elif packet.get("packet_name") == "SetPlayerPosition":
                        on_ground = packet.get("on_ground")
                        currentX = struct.unpack('>d', packet.get("x"))[0]
                        currentY = struct.unpack('>d', packet.get("y"))[0]
                        currentZ = struct.unpack('>d', packet.get("z"))[0]

                        general_player_handler.set_position(entity_id, (currentX, currentY, currentZ))

                        delta_x = int((currentX * 32 - prevX * 32) * 128)
                        delta_y = int((currentY * 32 - prevY * 32) * 128)
                        delta_z = int((currentZ * 32 - prevZ * 32) * 128)

                        update_entity_position = UpdateEntityPosition(entity_id, delta_x, delta_y, delta_z, on_ground)

                        networking.send_to_others(update_entity_position, client_socket, gamestate)

                    elif packet.get("packet_name") == "SetPlayerPositionRotation":
                        on_ground = packet.get("on_ground")
                        currentX = struct.unpack('>d', packet.get("x"))[0]
                        currentY = struct.unpack('>d', packet.get("y"))[0]
                        currentZ = struct.unpack('>d', packet.get("z"))[0]
                        yaw = packet.get("yaw")
                        pitch = packet.get("pitch")

                        general_player_handler.set_position(entity_id, (currentX, currentY, currentZ))

                        yaw = struct.unpack('>f', yaw)[0]
                        pitch = struct.unpack('>f', pitch)[0]

                        yaw = int((yaw / 360.0) * 256.0) & 0xff #convert
                        pitch = int((pitch / 360.0) * 256.0) & 0xff #convert

                        general_player_handler.set_rotation(entity_id, (pitch, yaw))

                        yaw = struct.pack("B", yaw)
                        pitch = struct.pack("B", pitch)

                        delta_x = int((currentX * 32 - prevX * 32) * 128)
                        delta_y = int((currentY * 32 - prevY * 32) * 128)
                        delta_z = int((currentZ * 32 - prevZ * 32) * 128)

                        update_entity_position_rotation = UpdateEntityPositionRotation(entity_id, delta_x, delta_y, delta_z, yaw, pitch, on_ground)

                        networking.send_to_others(update_entity_position_rotation, client_socket, gamestate)

                        set_head_rotation = SetHeadRotation(entity_id, yaw)

                        networking.send_to_others(set_head_rotation, client_socket, gamestate)

                    elif packet.get("packet_name") == "SetPlayerRotation":
                        on_ground = packet.get("on_ground")
                        yaw = packet.get("yaw")
                        pitch = packet.get("pitch")

                        yaw = struct.unpack('>f', yaw)[0]
                        pitch = struct.unpack('>f', pitch)[0]

                        yaw = int((yaw / 360.0) * 256.0) & 0xff #convert
                        pitch = int((pitch / 360.0) * 256.0) & 0xff #convert

                        general_player_handler.set_rotation(entity_id, (pitch, yaw))

                        yaw = struct.pack("B", yaw)
                        pitch = struct.pack("B", pitch)

                        update_entity_rotation = UpdateEntityRotation(entity_id, yaw, pitch, on_ground)

                        networking.send_to_others(update_entity_rotation, client_socket, gamestate)

                        set_head_rotation = SetHeadRotation(entity_id, yaw)

                        networking.send_to_others(set_head_rotation, client_socket, gamestate)
                    elif packet.get("packet_name") == "SwingArm":
                        hand = packet.get("hand")

                        if hand == 0:
                            animation = 0

                        elif hand == 1:
                            animation = 3

                        entity_animation = EntityAnimation(entity_id, animation)

                        networking.send_to_others(entity_animation, client_socket, gamestate)
                    elif packet.get("packet_name") == "PlayerCommand":
                        action_id = packet.get("action_id")

                        bit_mask = 0
                        value = b''

                        if action_id == 0:
                            value = b'\x05'
                            bit_mask |= 0x02
                        if action_id == 1:
                            value = b'\x00'
                        if action_id == 3:
                            bit_mask |= 0x08
                        #if action_id == 4:
                        #    pass
                        # Player stops sprinting (no bitmask needed)

                        bit_mask = struct.pack("B", bit_mask)

                        entries = []
                        entries.append({"index": 0, "value_type": 0, "value": bit_mask})
                        entries.append({"index": 6, "value_type": 20, "value": value}) if value != b'' else None

                        set_entity_metadata = SetEntityMetadata(packet.get("entity_id"), entries)

                        networking.send_to_others(set_entity_metadata, client_socket, gamestate)
                    elif packet.get("packet_name") == "PlayerAction":
                        acknowledge_block_change = AcknowledgeBlockChange(packet.get("sequence_id"))

                        clientbound.send(acknowledge_block_change, gamestate)

                        #TODO: add break speed checker
                        block_update = BlockUpdate(packet.get("position"), 0)

                        networking.send_to_others(block_update, client_socket, gamestate)

                        world_event = WorldEvent(2001, packet.get("position"), 1, False)

                        networking.send_to_others(world_event, client_socket, gamestate)
                        print("Player Action")

            threading.Thread(target=keepListening).start()

            def updateTab():
                pass
                #set_tablist_header_footer = SetTabListHeaderFooter("H", "A")

                #networking.broadcast(set_tablist_header_footer, gamestate)s

            threading.Thread(target=updateTab).start()

    networking = Networking()

    general_player_handler = GeneralPlayerHandler()

    while True:
        client_socket, address = server_socket.accept()

        new_connection = threading.Thread(target=handle, args=(client_socket, networking))
        new_connection.start()

if __name__ == "__main__":
    main()