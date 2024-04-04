import json
from Packets.PacketUtil import pack_data

class StatusResponse:
    def __init__(self, server_data):
        server_data = bytes(json.dumps(server_data), encoding="utf-8")

        self.json_data = pack_data(server_data)