from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class SpawnEntity(Packet):
    @enforce_annotations
    def __init__(self, entity_id: int, entity_uuid: bytes, entity_type: int, x: int, y: int, z: int, pitch: int, yaw: int, head_yaw: int, data: int, velocity_x: int, velocity_y: int, velocity_z: int):
        return super().__init__(entity_id, entity_uuid, entity_type, x, y, z, pitch, yaw, head_yaw, data, velocity_x, velocity_y, velocity_z)