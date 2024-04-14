from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class EncryptionRequest(Packet):
    @enforce_annotations
    def __init__(self, server_id: str, public_key: bytes, verify_token: bytes):
        return super().__init__(server_id, public_key, verify_token)
