from Packets.PacketUtil import pack_varint

class SetCenterChunk:
    def __init__(self, x, z):
        x = pack_varint(x)
        z = pack_varint(z)


        self.x = x
        self.z = z