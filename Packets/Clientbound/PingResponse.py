from Util import enforce_annotations
from Packets.PacketUtil import Packet

class PingResponse(Packet):
    @enforce_annotations
    def __init__(self, time: bytes):
        return super().__init__(time)