from Packets.PacketUtil import pack_varint
import struct

def encode_coordinates(x, z, y):
    # Ensure values are within range
    x &= 0x3FFFFFF  # 26 bits mask
    z &= 0x3FFFFFF  # 26 bits mask
    y &= 0xFFF      # 12 bits mask

    # Combine the values into a single 64-bit integer
    encoded_value = (x << 38) | (z << 12) | y

    # If the highest bit of each coordinate is set (indicating negative value), convert to two"s complement
    if x & 0x2000000:
        x -= 0x4000000
    if z & 0x2000000:
        z -= 0x4000000
    if y & 0x800:
        y -= 0x1000

    return encoded_value
class SetDefaultSpawnPosition:
    def __init__(self, x, y, z, angle):
        encoded_coordinates = encode_coordinates(x, z, y)
        location = struct.pack(">Q", encoded_coordinates)

        angle = struct.pack("f", angle)

        self.location = location
        self.angle = angle




