from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class BlockUpdate(Packet):
    @enforce_annotations
    def __init__(self, location, block_id):
        return super().__init__(location, block_id)