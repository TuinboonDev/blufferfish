from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class EntityAnimation(Packet):
    @enforce_annotations
    def __init__(self, entity_id, animation):
        return super().__init__(entity_id, animation)