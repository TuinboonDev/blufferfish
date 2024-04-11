from Packets.PacketUtil import pack_varint
from Util import enforce_annotations

class UpdateEntityRotation:
    @enforce_annotations
    def __init__(self, entity_id: int, yaw: bytes, pitch: bytes, on_ground: bytes):
        entity_id = pack_varint(entity_id)

        self.entity_id = entity_id
        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground