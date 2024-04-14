from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class ConfigurationFinish(Packet):
    @enforce_annotations
    def __init__(self):
        return super().__init__()