from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class UpdateEntityPositionRotation(Packet):
    @enforce_annotations
    def __init__(self, entity_id: int, delta_x: int, delta_y: int, delta_z: int, yaw: bytes, pitch: bytes, on_ground: bytes):
        return super().__init__(entity_id, delta_x, delta_y, delta_z, yaw, pitch, on_ground)