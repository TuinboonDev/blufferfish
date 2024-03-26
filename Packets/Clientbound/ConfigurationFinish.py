from Packets.PacketUtil import pack_varint

class ConfigurationFinish:
    def __init__(self):
        packet_id = pack_varint(0x02)

        self.packet_id = packet_id