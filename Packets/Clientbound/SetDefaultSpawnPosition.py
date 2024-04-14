from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class SetDefaultSpawnPosition(Packet):
    @enforce_annotations
    def __init__(self, x: int, y: int, z: int, angle: int):
        return super().__init__(x, y, z, angle)