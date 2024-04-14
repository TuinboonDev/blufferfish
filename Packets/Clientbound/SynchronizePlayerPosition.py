from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class SynchronizePlayerPosition(Packet):
    @enforce_annotations
    def __init__(self, x: int, y: int, z: int, yaw: int, pitch: int, flags: bytes, teleport_id: int):
        return super().__init__(x, y, z, yaw, pitch, flags, teleport_id)