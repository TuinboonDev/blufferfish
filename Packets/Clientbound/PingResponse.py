from Packets.PacketUtil import pack_varint, write_string

class PingResponse:
    def __init__(self, time):
        self.time = time