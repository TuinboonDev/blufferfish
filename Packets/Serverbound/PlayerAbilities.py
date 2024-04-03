from Packets.PacketUtil import unpack_encrypted_varint

class PlayerAbilities:
    def create(self, remaining_packet_length, socket):
        flags = unpack_encrypted_varint(socket)

        self.flags = flags
        return self

    def get(self, item):
        return self.__dict__[item]