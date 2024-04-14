from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class UpdateEntityRotation(Packet):
    @enforce_annotations
    def __init__(self, entity_id: int, yaw: bytes, pitch: bytes, on_ground: bytes):
        return super().__init__(entity_id, yaw, pitch, on_ground)