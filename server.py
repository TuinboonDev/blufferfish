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
from Packets.Clientbound.OpenBook import OpenBook
from Packets.Clientbound.DisplayObjective import DisplayObjective
from Packets.Clientbound.PlayerInfoUpdate import PlayerInfoUpdate
from Packets.Clientbound.SpawnEntity import SpawnEntity

from Packets.PacketHandler import Clientbound, Serverbound
from Packets.PacketUtil import unpack_varint, unpack_encrypted_varint, pack_varint, unpack_varint_bytes
from Packets.ServerData import ServerData
from Packets.PacketMap import set_gamestate, get_gamestate

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

    def get_packet(socket):
        packet_length = unpack_varint(socket)
        packet_id = unpack_varint(socket)
        return serverbound.receive(packet_id)

    def get_encrypted_packet(socket, decryptor):
        packet_length = unpack_encrypted_varint(socket)
        packet_id = unpack_encrypted_varint(socket)
        return serverbound.receive(packet_id)

    while True:
        client_socket, address = server_socket.accept()

        clientbound = Clientbound(client_socket)
        serverbound = Serverbound(client_socket)

        set_gamestate("HANDSHAKE")

        print("Connection from", address)

        if get_gamestate() == "HANDSHAKE":
            packet = get_packet(client_socket)

            if isinstance(packet, Handshake):
                if packet.get("next_state") == 1:
                    set_gamestate("STATUS")
                elif packet.get("next_state") == 2:
                    set_gamestate("LOGIN")

        if get_gamestate() == "STATUS":
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

        if get_gamestate() == "LOGIN":
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

                    verification_hash = sha1()

                    verification_hash.update(server_id.encode('utf-8'))
                    verification_hash.update(shared_secret)
                    verification_hash.update(public_key_der)

                    number_representation = int.from_bytes(verification_hash.digest(), byteorder='big', signed=True)
                    hash = format(number_representation, 'x')

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

                        Packets.PacketUtil.decryptor = decryptor

                        login_success = LoginSuccess(uuid_bytes, name, b'')

                        clientbound.send_encrypted(login_success, encryptor)

                print("Sent login success")

                #LOGIN ACKNOWLEDGEMENT
                packet = get_encrypted_packet(client_socket, decryptor)
                if isinstance(packet, LoginAcknowledged):
                    set_gamestate("CONFIGURATION")
                    print("Login Acknowledged")

        if get_gamestate() == "CONFIGURATION":
            packet = get_encrypted_packet(client_socket, decryptor)

            if isinstance(packet, ServerboundPluginMessage):
                print("Plugin Message")

            # Registry Data

            registry_data = RegistryData()

            clientbound.send_encrypted(registry_data, encryptor)

            # configuration finish

            configfinish = ConfigurationFinish()

            clientbound.send_encrypted(configfinish, encryptor)

            packet = get_encrypted_packet(client_socket, decryptor)

            if isinstance(packet, AcknowledgeFinishConfiguration):
                set_gamestate("PLAY")
                print("Configuration Finished")

        if get_gamestate() == "PLAY":

            login_play = LoginPlay(
                1,
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

            clientbound.send_encrypted(login_play, encryptor)

            print("Login Success")

            teleport_id = 123

            sync_player_pos = SyncronizePlayerPosition(10, 100, 10, 0, 0, b'\x00', teleport_id)

            clientbound.send_encrypted(sync_player_pos, encryptor)

            # Set default spawn pos

            set_default_spawn_pos = SetDefaultSpawnPosition(0, 0, 0, 0)

            clientbound.send_encrypted(set_default_spawn_pos, encryptor)

            # Game event packet

            game_event = GameEvent(13, 0)

            clientbound.send_encrypted(game_event, encryptor)

            # Center chunk

            set_center_chunk = SetCenterChunk(0, 0)

            clientbound.send_encrypted(set_center_chunk, encryptor)

            # Chunk Data and Update Light

            chunk_data_update_light = ChunkDataUpdateLight(0, 0, b'', b'')
            clientbound.send_encrypted(chunk_data_update_light, encryptor)

            # tp confirm
            packet = get_encrypted_packet(client_socket, decryptor)

            if isinstance(packet, ConfirmTeleportation):
                if packet.get("teleport_id") == teleport_id:
                    print("Teleportation confirmed")

            def keepAlive():
                while True:
                    keep_alive = KeepAlive(123)

                    clientbound.send_encrypted(keep_alive, encryptor)
                    time.sleep(29)

            threading.Thread(target=keepAlive).start()

            add_player = PlayerInfoUpdate([0x01, 0x08], [{"uuid": uuid_bytes, "name": name, "show": True}],
                                          {"name": session_json["properties"][0]["name"],
                                           "value": session_json["properties"][0]["value"],
                                           "is_signed": True,
                                           "signature": session_json["properties"][0]["signature"]})

            clientbound.send_encrypted(add_player, encryptor)

            print('crazy?')

    # client_socket.close()

if __name__ == "__main__":
    main()