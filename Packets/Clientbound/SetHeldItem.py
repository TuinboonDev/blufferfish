from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class SetHeldItem(Packet):
    @enforce_annotations
    def __init__(self, slot):
        return super().__init__(slot)