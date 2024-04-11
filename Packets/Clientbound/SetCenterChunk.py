from Packets.PacketUtil import pack_varint
from Util import enforce_annotations

class SetCenterChunk:
    @enforce_annotations
    def __init__(self, x: int, z: int):
        x = pack_varint(x)
        z = pack_varint(z)


        self.x = x
        self.z = z