from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

import json

Pack = Pack()

class StatusResponse(Packet):
    @enforce_annotations
    def __init__(self, server_data: dict):
        return super().__init__(server_data)
