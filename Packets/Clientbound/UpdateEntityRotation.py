import struct
from Packets.PacketUtil import pack_varint, pack_data

class UpdateEntityRotation:
    def __init__(self, entity_id, yaw, pitch, on_ground):
        entity_id = pack_varint(entity_id)

        self.entity_id = entity_id
        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground