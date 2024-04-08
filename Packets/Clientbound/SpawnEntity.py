from Packets.PacketUtil import pack_varint
import struct

class SpawnEntity:
    def __init__(self, entity_id, entity_uuid, entity_type, x, y, z, pitch, yaw, head_yaw, data, velocity_x, velocity_y, velocity_z):
        entity_id = pack_varint(entity_id)

        entity_type = pack_varint(entity_type)

        x = struct.pack('>d', x)
        y = struct.pack('>d', y)
        z = struct.pack('>d', z)

        pitch = struct.pack('B', pitch)
        yaw = struct.pack('B', yaw)
        head_yaw = struct.pack('B', head_yaw)

        data = pack_varint(data)

        velocity_x = struct.pack('h', velocity_x)
        velocity_y = struct.pack('h', velocity_y)
        velocity_z = struct.pack('h', velocity_z)

        self.entity_id = entity_id
        self.entity_uuid = entity_uuid
        self.entity_type = entity_type
        self.x = x
        self.y = y
        self.z = z
        self.pitch = pitch
        self.yaw = yaw
        self.head_yaw = head_yaw
        self.data = data
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.velocity_z = velocity_z