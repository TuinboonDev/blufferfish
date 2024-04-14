from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class SetCenterChunk(Packet):
    @enforce_annotations
    def __init__(self, x: int, y: int):
        return super().__init__(x, y)