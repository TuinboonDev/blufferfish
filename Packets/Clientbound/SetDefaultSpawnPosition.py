from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class SetDefaultSpawnPosition(Packet):
    @enforce_annotations
    def __init__(self, location: tuple, angle: int):
        return super().__init__(location, angle)