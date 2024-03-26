from Packets.PacketUtil import pack_varint

class RegistryData:
    def __init__(self):
        registry_data = open("registry_info.packet", "rb").read()
        packet_id = pack_varint(0x05)

        self.packet_id = packet_id
        self.registry_data = registry_data