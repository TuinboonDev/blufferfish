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
            print(GameStates)
            print(f"Error: {state} is not a valid gamestate")

    def get_gamestate(self):
        return self.gamestate

Unpack = Unpack()
Pack = Pack()

class PacketPayloads:
    class Unpack:
        class ENCRYPTED:
            VARINT = Unpack.unpack_varint
            STRING = Unpack.unpack_string
            BYTE = Unpack.unpack_encrypted_byte
            SHORT = Unpack.unpack_encrypted_short
            UNSIGNED_SHORT = Unpack.unpack_unsigned_short
            LONG = Unpack.unpack_encrypted_long

        class UNENCRYPTED:
            VARINT = Unpack.unpack_varint
            STRING = Unpack.unpack_string
            BYTE = Unpack.unpack_byte
            SHORT = Unpack.unpack_short
            UNSIGNED_SHORT = Unpack.unpack_unsigned_short
            LONG = Unpack.unpack_long

    class Pack:
        VARINT = Pack.pack_varint
        STRING = Pack.write_string
        BYTE = 1
        SHORT = 1
        UNSIGNED_SHORT = 1
        LONG = Pack.pack_long

Pack = PacketPayloads.Pack
Unpack = PacketPayloads.Unpack

GameStates = {
    "HANDSHAKE": {
        "C2S": {
            0x00: [{"name": "Handshake"}, {"protocol_version": Unpack.ENCRYPTED.VARINT}, {"server_address": Unpack.UNENCRYPTED.STRING}, {"server_port": Unpack.UNENCRYPTED.UNSIGNED_SHORT}, {"next_state": Unpack.UNENCRYPTED.VARINT}]
        }
    },

    "STATUS": {
        "C2S": {
            0x00: [{"name": "StatusRequest"}],
            0x01: [{"name": "PingRequest"}, {"time": Unpack.UNENCRYPTED.LONG}]
        },
        "S2C": {
            0x00: [{"class": StatusResponse}, {"response": Pack.STRING}],
            0x1: [{"class": PingResponse}, {"time": Pack.LONG}]
        }
    },


    "LOGIN": {}}
"""
        "C2S": {
            0x00: LoginStart,
            0x01: EncryptionResponse,
            0x03: LoginAcknowledged
        },
        "S2C": {
            0x01: EncryptionRequest,
            0x02: LoginSuccess
        }
    },

    "CONFIGURATION": {
        "C2S": {
            0x00: ClientInformation,
            0x01: ServerboundPluginMessage,
            0x02: AcknowledgeFinishConfiguration
        },
        "S2C": {
            0x02: ConfigurationFinish,
            0x05: RegistryData
        }
    },

    "PLAY": {
        "C2S": {
            0x21: PlayerAction,
            0x10: ServerboundPluginMessage,
            0x20: PlayerAbilities,
            0x33: SwingArm,
            0x22: PlayerCommand,
            0x15: ServerboundKeepAlive,
            0x19: SetPlayerRotation,
            0x1A: SetPlayerOnGround,
            0x06: PlayerSession,
            0x18: SetPlayerPositionRotation,
            0x17: SetPlayerPosition,
            0x00: ConfirmTeleportation
        },
        "S2C": {
            0x6A: SetTabListHeaderFooter,
            0x26: WorldEvent,
            0x09: BlockUpdate,
            0x05: AcknowledgeBlockChange,
            0x03: EntityAnimation,
            0x46: SetHeadRotation,
            0x2D: UpdateEntityPositionRotation,
            0x2E: UpdateEntityRotation,
            0x51: SetHeldItem,
            0x2C: UpdateEntityPosition,
            0x01: SpawnEntity,
            0x3C: PlayerInfoUpdate,
            0x55: DisplayObjective,
            0x30: OpenBook,
            0x29: LoginPlay,
            0x3E: SyncronizePlayerPosition,
            0x54: SetDefaultSpawnPosition,
            0x52: SetCenterChunk,
            0x25: ChunkDataUpdateLight,
            0x20: GameEvent,
            0x24: KeepAlive,
            0x56: SetEntityMetadata
        }
    }
}
"""