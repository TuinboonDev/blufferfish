from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class AcknowledgeBlockChange(Packet):
    @enforce_annotations
    def __init__(self, sequence_id):
        return super().__init__(sequence_id)