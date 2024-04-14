"""
from Packets.Serverbound.StatusRequest import StatusRequest
from Packets.Serverbound.EncryptionResponse import EncryptionResponse
from Packets.Serverbound.PingRequest import PingRequest
from Packets.Serverbound.Handshake import Handshake
from Packets.Serverbound.LoginStart import LoginStart
from Packets.Serverbound.LoginAcknowledged import LoginAcknowledged
from Packets.Serverbound.ServerboundPluginMessage import ServerboundPluginMessage
from Packets.Serverbound.AcknowledgeFinishConfiguration import AcknowledgeFinishConfiguration
from Packets.Serverbound.ConfirmTeleportation import ConfirmTeleportation
from Packets.Serverbound.ClientInformation import ClientInformation
from Packets.Serverbound.SetPlayerPosition import SetPlayerPosition
from Packets.Serverbound.SetPlayerPositionRotation import SetPlayerPositionRotation
from Packets.Serverbound.PlayerSession import PlayerSession
from Packets.Serverbound.SetPlayerOnGround import SetPlayerOnGround
from Packets.Serverbound.SetPlayerRotation import SetPlayerRotation
from Packets.Serverbound.ServerboundKeepAlive import ServerboundKeepAlive
from Packets.Serverbound.PlayerCommand import PlayerCommand
from Packets.Serverbound.SwingArm import SwingArm
from Packets.Serverbound.PlayerAbilities import PlayerAbilities
from Packets.Serverbound.PlayerAction import PlayerAction

from Packets.Clientbound.SetTabListHeaderFooter import SetTabListHeaderFooter
from Packets.Clientbound.WorldEvent import WorldEvent
from Packets.Clientbound.BlockUpdate import BlockUpdate
from Packets.Clientbound.AcknowledgeBlockChange import AcknowledgeBlockChange
from Packets.Clientbound.SetHeadRotation import SetHeadRotation
from Packets.Clientbound.LoginSuccess import LoginSuccess
from Packets.Clientbound.EncryptionRequest import EncryptionRequest
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
from Packets.Clientbound.SetEntityMetadata import SetEntityMetadata
from Packets.Clientbound.UpdateEntityPosition import UpdateEntityPosition
from Packets.Clientbound.SetHeldItem import SetHeldItem
from Packets.Clientbound.UpdateEntityPositionRotation import UpdateEntityPositionRotation
from Packets.Clientbound.UpdateEntityRotation import UpdateEntityRotation
from Packets.Clientbound.EntityAnimation import EntityAnimation
"""
from Packets.Clientbound.PingResponse import PingResponse
from Packets.Clientbound.StatusResponse import StatusResponse

from Util import enforce_annotations
from Packets.PacketUtil import Unpack, Pack

class GameState:
    def __init__(self):
        self.gamestate = "HANDSHAKE"

    @enforce_annotations
    def set_gamestate(self, state: str):
        if state in GameStates:
            self.gamestate = state
        else:
            #print(GameStates)
            print(f"Error: {state} is not a valid gamestate")

    def get_gamestate(self):
        return self.gamestate

Unpack = Unpack()
Pack = Pack()

class PacketPayloads:
    class Unpack:
        class ENCRYPTED:
            VARINT = Unpack.unpack_encrypted_varint
            STRING = Unpack.unpack_encrypted_string
            BYTE = Unpack.unpack_encrypted_byte
            SHORT = Unpack.unpack_encrypted_short
            UNSIGNED_SHORT = Unpack.unpack_encrypted_unsigned_short
            LONG = Unpack.unpack_encrypted_long
            UUID = Unpack.unpack_encrypted_uuid
            DATA = Unpack.unpack_encrypted_data
            REMAINING = Unpack.unpack_encrypted_remaining
            LOCATION = Unpack.unpack_encrypted_location
            FLOAT = Unpack.unpack_encrypted_float
            DOUBLE = Unpack.unpack_encrypted_double

        class UNENCRYPTED:
            VARINT = Unpack.unpack_varint
            STRING = Unpack.unpack_string
            BYTE = Unpack.unpack_byte
            SHORT = Unpack.unpack_short
            UNSIGNED_SHORT = Unpack.unpack_unsigned_short
            LONG = Unpack.unpack_long
            UUID = Unpack.unpack_uuid
            DATA = Unpack.unpack_data

    class Pack:
        VARINT = Pack.pack_varint
        STRING = Pack.write_string
        BYTE = Pack.pack_byte
        SHORT = 1
        UNSIGNED_SHORT = 1
        LONG = Pack.pack_long
        DATA = Pack.pack_data
        INT = Pack.pack_int
        LOCATION = Pack.pack_location
        ANGLE = Pack.pack_angle
        DOUBLE = Pack.pack_double
        PLAYERS = Pack.pack_players
        GAMEMODE = Pack.pack_gamemode
        FLOAT = Pack.pack_float

Pack = PacketPayloads.Pack
Unpack = PacketPayloads.Unpack

GameStates = {
    "HANDSHAKE": {
        "C2S": {
            0x00: {"Handshake": [{"protocol_version": Unpack.UNENCRYPTED.VARINT}, {"server_address": Unpack.UNENCRYPTED.STRING}, {"server_port": Unpack.UNENCRYPTED.UNSIGNED_SHORT}, {"next_state": Unpack.UNENCRYPTED.VARINT}]}
        }
    },

    "STATUS": {
        "C2S": {
            0x00: {"StatusRequest": []},
            0x01: {"PingRequest": [{"time": Unpack.UNENCRYPTED.LONG}]}
        },
        "S2C": {
            0x00: {"StatusResponse": [{"response": Pack.STRING}]},
            0x01: {"PingResponse": [{"time": Pack.LONG}]}
        }
    },


    "LOGIN": {
        "C2S": {
            0x00: {"LoginStart": [{"name": Unpack.UNENCRYPTED.STRING}, {"uuid": Unpack.UNENCRYPTED.UUID}]},
            0x01: {"EncryptionResponse": [{"shared_secret": Unpack.UNENCRYPTED.DATA}, {"verify_token": Unpack.UNENCRYPTED.DATA}]},
            0x03: {"LoginAcknowledged": []}
        },
        "S2C": {
            0x01: {"EncryptionRequest": [{"server_id": Pack.STRING}, {"public_key": Pack.DATA}, {"verify_token": Pack.DATA}]},
            0x02: {"LoginSuccess": [{"uuid": Pack.BYTE}, {"name": Pack.STRING}, {"properties": Pack.DATA}]}
        }
    },

    "CONFIGURATION": {
        "C2S": {
            0x00: {"ClientInformation": [{"locale": Unpack.ENCRYPTED.STRING}, {"view_distance": Unpack.ENCRYPTED.BYTE}, {"chat_mode": Unpack.ENCRYPTED.VARINT}, {"chat_colors": Unpack.ENCRYPTED.BYTE}, {"displayed_skin_parts": Unpack.ENCRYPTED.BYTE}, {"main_hand": Unpack.ENCRYPTED.VARINT}, {"enable_text_filtering": Unpack.ENCRYPTED.BYTE}, {"allow_server_listing": Unpack.ENCRYPTED.BYTE}]},
            0x01: {"ServerboundPluginMessage": [{"channel": Unpack.ENCRYPTED.STRING}, {"data": Unpack.ENCRYPTED.REMAINING}]},
            0x02: {"AcknowledgeFinishConfiguration": []}
        },
        "S2C": {
            0x02: {"ConfigurationFinish": []},
            0x05: {"RegistryData": [{"data": Pack.BYTE}]}
        }
    },

    "PLAY": {
        "C2S": {
            0x21: {"PlayerAction": [{"status": Unpack.ENCRYPTED.VARINT}, {"location": Unpack.ENCRYPTED.LOCATION}, {"face": Pack.BYTE}, {"sequence": Pack.VARINT}]},
            0x10: {"ServerboundPluginMessage": [{"channel": Unpack.ENCRYPTED.STRING}, {"data": Unpack.ENCRYPTED.REMAINING}]},
            0x20: {"PlayerAbilities": [{"flags": Unpack.ENCRYPTED.BYTE}]},
            0x33: {"SwingArm": [{"hand": Unpack.ENCRYPTED.VARINT}]},
            0x22: {"PlayerCommand": [{"entity_id": Unpack.ENCRYPTED.VARINT}, {"action_id": Unpack.ENCRYPTED.VARINT}, {"jump_boost": Unpack.ENCRYPTED.VARINT}]},
            0x15: {"ServerboundKeepAlive": [{"keep_alive_id": Unpack.ENCRYPTED.LONG}]},
            0x19: {"SetPlayerRotation": [{"yaw": Unpack.ENCRYPTED.FLOAT}, {"pitch": Unpack.ENCRYPTED.FLOAT}, {"on_ground": Unpack.ENCRYPTED.BYTE}]},
            0x1A: {"SetPlayerOnGround": [{"on_ground": Unpack.ENCRYPTED.BYTE}]},
            0x06: {"PlayerSession": [{"session_id": Unpack.ENCRYPTED.UUID}, {"expires_at": Unpack.ENCRYPTED.LONG}, {"public_key": Unpack.ENCRYPTED.DATA}, {"key_signature": Unpack.ENCRYPTED.DATA}]},
            0x18: {"SetPlayerPositionRotation": [{"x": Unpack.ENCRYPTED.DOUBLE}, {"y": Unpack.ENCRYPTED.DOUBLE}, {"z": Unpack.ENCRYPTED.DOUBLE}, {"yaw": Unpack.ENCRYPTED.FLOAT}, {"pitch": Unpack.ENCRYPTED.FLOAT}, {"on_ground": Unpack.ENCRYPTED.BYTE}]},
            0x17: {"SetPlayerPosition": [{"x": Unpack.ENCRYPTED.DOUBLE}, {"y": Unpack.ENCRYPTED.DOUBLE}, {"z": Unpack.ENCRYPTED.DOUBLE}, {"on_ground": Unpack.ENCRYPTED.BYTE}]},
            0x00: {"ConfirmTeleportation": [{"teleport_id": Unpack.ENCRYPTED.VARINT}]},
        },

        "S2C": {
            #TODO: text component parsing
            0x6A: {"SetTabListHeaderFooter": [{"header": Pack.STRING}, {"footer": Pack.STRING}]},

            0x26: {"WorldEvent": [{"event": Pack.INT}, {"position": Pack.LOCATION}, {"data": Pack.INT}, {"disable_relative_volume": Pack.BYTE}]},
            0x09: {"BlockUpdate": [{"location": Pack.LOCATION}, {"block_id": Pack.VARINT}]},
            0x05: {"AcknowledgeBlockChange": [{"sequence_id": Pack.VARINT}]},
            0x03: {"EntityAnimation": [{"entity_id": Pack.VARINT}, {"animation": Pack.BYTE}]},
            0x46: {"SetHeadRotation": [{"entity_id": Pack.VARINT}, {"head_yaw": Pack.ANGLE}]},
            0x2D: {"UpdateEntityPositionRotation": [{"entity_id": Pack.VARINT}, {"delta_x": Pack.SHORT}, {"delta_y": Pack.SHORT}, {"delta_z": Pack.SHORT}, {"yaw": Pack.ANGLE}, {"pitch": Pack.ANGLE}, {"on_ground": Pack.BYTE}]},
            0x2E: {"UpdateEntityRotation": [{"entity_id": Pack.VARINT}, {"yaw": Pack.ANGLE}, {"pitch": Pack.ANGLE}, {"on_ground": Pack.BYTE}]},
            0x51: {"SetHeldItem": [{"slot": Pack.BYTE}]},
            0x2C: {"UpdateEntityPosition": [{"entity_id": Pack.VARINT}, {"delta_x": Pack.SHORT}, {"delta_y": Pack.SHORT}, {"delta_z": Pack.SHORT}, {"on_ground": Pack.BYTE}]},
            0x01: {"SpawnEntity": [{"entity_id": Pack.VARINT}, {"entity_uuid": Pack.BYTE}, {"type": Pack.VARINT}, {"x": Pack.DOUBLE}, {"y": Pack.DOUBLE}, {"z": Pack.DOUBLE}, {"pitch": Pack.ANGLE}, {"yaw": Pack.ANGLE}, {"head_pitch": Pack.ANGLE}, {"data": Pack.VARINT}, {"velocity_x": Pack.SHORT}, {"velocity_y": Pack.SHORT}, {"velocity_z": Pack.SHORT}]},

            #TODO: I DIDNT EVEN REDO THIS PACKET I AM LAZY
            0x3C: {"PlayerInfoUpdate": [{"WHOLEPACKETPLSHELP": Pack.BYTE}]},
            0x55: {"DisplayObjective": [{"position": Pack.VARINT}, {"score_name": Pack.STRING}]},
            0x30: {"OpenBook": [{"hand": Pack.VARINT}]},
            0x29: {"LoginPlay": [{"entity_id": Pack.INT}, {"is_hardcore": Pack.BYTE}, {"dimensions": Pack.DATA}, {"max_players": Pack.VARINT}, {"view_distance": Pack.VARINT}, {"simulation_distance": Pack.VARINT}, {"reduced_debug_info": Pack.BYTE}, {"respawn_screen": Pack.BYTE}, {"limited_crafting": Pack.BYTE}, {"dimension_typ": Pack.STRING}, {"dimension_name": Pack.STRING}, {"seed": Pack.LONG}, {"gamemode": Pack.GAMEMODE}, {"previous_gamemode": Pack.GAMEMODE}, {"is_debug": Pack.BYTE}, {"is_flat": Pack.BYTE}, {"has_death_location": Pack.BYTE}, {"portal_cooldown": Pack.VARINT}]},
            0x3E: {"SyncronizePlayerPosition": [{"x": Pack.DOUBLE}, {"y": Pack.DOUBLE}, {"z": Pack.DOUBLE}, {"yaw": Pack.FLOAT}, {"pitch": Pack.FLOAT}, {"flags": Pack.BYTE}, {"teleport_id": Pack.VARINT}]},
            0x54: {"SetDefaultSpawnPosition": [{"location": Pack.LOCATION}, {"angle": Pack.FLOAT}]},
            0x52: {"SetCenterChunk": [{"chunk_x": Pack.VARINT}, {"chunk_z": Pack.VARINT}]},

            #TODO: I DIDNT EVEN REDO THIS PACKET I AM LAZY
            #TODO: IM SO LAZY I COPIED THIS LINE ^
            0x25: {"ChunkDataUpdateLight": [{"WHOLEPACKETAGAIN": Pack.BYTE}]},
            0x20: {"GameEvent": [{"event": Pack.BYTE}, {"value": Pack.FLOAT}]},
            0x24: {"KeepAlive": [{"keep_alive_id": Pack.LONG}]},
            0x56: {"SetEntityMetadata": [{"entity_id": Pack.VARINT}, {"metadata": Pack.DATA}]}
        }
    }
}