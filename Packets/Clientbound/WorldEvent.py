from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class WorldEvent(Packet):
    @enforce_annotations
    def __init__(self, event_id, location, data, disable_relative_volume):
        return super().__init__(event_id, location, data, disable_relative_volume)