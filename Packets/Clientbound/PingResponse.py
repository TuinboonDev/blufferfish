from Packets.PacketUtil import pack_varint, write_string

class PingResponse:
    def __init__(self, time):
        packet_id = pack_varint(0x01)

        self.packet_id = packet_id
        self.time = time