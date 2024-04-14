from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class UpdateEntityPosition(Packet):
    @enforce_annotations
    def __init__(self, entity_id, delta_x, delta_y, delta_z, on_ground):
        return super().__init__(entity_id, delta_x, delta_y, delta_z, on_ground)