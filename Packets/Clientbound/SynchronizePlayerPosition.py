from Packets.PacketUtil import pack_varint
from Util import enforce_annotations

import struct

class SyncronizePlayerPosition:
    @enforce_annotations
    def __init__(self, x: int, y: int, z: int, yaw: int, pitch: int, flags: bytes, teleport_id: int):
        double_x = struct.pack('>d', x)
        double_y = struct.pack('>d', y)
        double_z = struct.pack('>d', z)

        float_yaw = struct.pack('f', yaw)
        float_pitch = struct.pack('f', pitch)

        teleport_id = pack_varint(teleport_id)

        self.x = double_x
        self.y = double_y
        self.z = double_z
        self.yaw = float_yaw
        self.pitch = float_pitch
        self.flags = flags
        self.teleport_id = teleport_id




