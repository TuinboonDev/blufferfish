from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class LoginSuccess(Packet):
    @enforce_annotations
    def __init__(self, uuid: bytes, username: str, properties: bytes):
        return super().__init__(uuid, username, properties)