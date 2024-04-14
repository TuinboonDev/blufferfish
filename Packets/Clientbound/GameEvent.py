from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class GameEvent(Packet):
    @enforce_annotations
    def __init__(self, event: int, value: int):
        return super().__init__(event, value)