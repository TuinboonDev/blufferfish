import json
from Packets.PacketUtil import pack_varint, pack_data

class StatusResponse:
    def __init__(self, server_data):
        server_data = bytes(json.dumps(server_data), encoding="utf-8")
        packet_id = pack_varint(0x00)

        self.packet_id = packet_id
        self.json_data = pack_data(server_data)