from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class RegistryData(Packet):
    @enforce_annotations
    def __init__(self, registry_data: bytes):
        return super().__init__(registry_data)