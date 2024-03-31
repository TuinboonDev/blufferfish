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

from Packets.Clientbound.StatusResponse import StatusResponse
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
from Packets.Clientbound.PingResponse import PingResponse
from Packets.Clientbound.OpenBook import OpenBook
from Packets.Clientbound.DisplayObjective import DisplayObjective
from Packets.Clientbound.PlayerInfoUpdate import PlayerInfoUpdate
from Packets.Clientbound.SpawnEntity import SpawnEntity
from Packets.Clientbound.SetEntityMetadata import SetEntityMetadata


gamestate = "HANDSHAKE"
def set_gamestate(state):
    if state in GameStates:
        global gamestate
        gamestate = state
    else:
        print(f"Error: {state} is not a valid gamestate")

def get_gamestate():
    return gamestate

GameStates = {
    "HANDSHAKE": {
        "C2S": {
            0x00: Handshake
        }
    },

    "STATUS": {
        "C2S": {
            0x00: StatusRequest,
            0x01: PingRequest
        },
        "S2C": {
            0x00: StatusResponse,
            0x1: PingResponse
        }
    },

    "LOGIN": {
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
            0x00: ConfirmTeleportation
        },
        "S2C": {
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