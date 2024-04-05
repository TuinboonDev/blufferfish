import struct
from Packets.PacketUtil import pack_varint

class EntityAnimation:
    def __init__(self, entity_id, animation):
        entity_id = pack_varint(entity_id)
        animation = struct.pack('B', animation)

        self.entity_id = entity_id
        self.animation = animation