from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class KeepAlive(Packet):
    @enforce_annotations
    def __init__(self, keep_alive_id: int):
        return super().__init__(keep_alive_id)