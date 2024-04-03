from Packets.PacketUtil import pack_varint
import struct

class UpdateEntityPosition:
    def __init__(self, entity_id, delta_x, delta_y, delta_z, on_ground):
        entity_id = pack_varint(entity_id)
        delta_x = struct.pack('>h', delta_x)
        delta_y = struct.pack('>h', delta_y)
        delta_z = struct.pack('>h', delta_z)


        self.entity_id = entity_id
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.delta_z = delta_z
        self.on_ground = on_ground