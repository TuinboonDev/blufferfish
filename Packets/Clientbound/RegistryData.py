from Packets.PacketUtil import pack_varint

class RegistryData:
    def __init__(self):
        registry_data = open("registry_info.packet", "rb").read()

        self.registry_data = registry_data