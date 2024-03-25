from Packets.Clientbound.StatusResponse import StatusResponse
from Packets.Serverbound.StatusRequest import StatusRequest
from Packets.Clientbound.PingResponse import PingResponse
from Packets.Serverbound.EncryptionResponse import EncryptionResponse
from Packets.Serverbound.PingRequest import PingRequest
from Packets.Serverbound.Handshake import Handshake
from Packets.Serverbound.LoginStart import LoginStart
from Packets.Serverbound.LoginAcknowledged import LoginAcknowledged
from Packets.Clientbound.LoginSuccess import LoginSuccess
from Packets.Clientbound.EncryptionRequest import EncryptionRequest
from Packets.Serverbound.ServerboundPluginMessage import ServerboundPluginMessage

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
        "S2C":{
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
            0x00: None,
            0x01: EncryptionRequest,
            0x02: LoginSuccess
        }
    },

    "CONFIGURATION": {
        "C2S": {
            0x01: ServerboundPluginMessage
        }
    }
}