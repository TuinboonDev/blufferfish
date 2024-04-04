from Packets.PacketUtil import pack_varint
import struct
class SynchronizePlayerPosition:
    def __init__(self, x, y, z, yaw, pitch, flags, teleport_id):
        double_x = struct.pack(">d", x)
        double_y = struct.pack(">d", y)
        double_z = struct.pack(">d", z)

        float_yaw = struct.pack("f", yaw)
        float_pitch = struct.pack("f", pitch)

        teleport_id = pack_varint(teleport_id)

        self.x = double_x
        self.y = double_y
        self.z = double_z
        self.yaw = float_yaw
        self.pitch = float_pitch
        self.flags = flags
        self.teleport_id = teleport_id




