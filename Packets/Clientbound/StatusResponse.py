from Packets.PacketUtil import pack_data
from Util import enforce_annotations

import json

class StatusResponse:
    @enforce_annotations
    def __init__(self, server_data: dict):
        server_data = bytes(json.dumps(server_data), encoding="utf-8")

        self.json_data = pack_data(server_data)