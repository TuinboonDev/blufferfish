from Packets.PacketUtil import pack_varint
from Util import enforce_annotations

import struct

class UpdateEntityPositionRotation:
    @enforce_annotations
    def __init__(self, entity_id: int, delta_x: int, delta_y: int, delta_z: int, yaw: bytes, pitch: bytes, on_ground: bytes):
        entity_id = pack_varint(entity_id)
        delta_x = struct.pack('>h', delta_x)
        delta_y = struct.pack('>h', delta_y)
        delta_z = struct.pack('>h', delta_z)

        self.entity_id = entity_id
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.delta_z = delta_z
        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground
