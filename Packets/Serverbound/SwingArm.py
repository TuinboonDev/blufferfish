from Packets.PacketUtil import unpack_encrypted_varint

class SwingArm:
    def create(self, remaining_packet_length, socket):
        hand = unpack_encrypted_varint(socket)

        self.hand = hand
        return self

    def get(self, item):
        return self.__dict__[item]