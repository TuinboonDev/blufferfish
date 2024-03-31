from Packets.PacketUtil import unpack_encrypted_varint

class ConfirmTeleportation:
    def create(self, remaining_packet_length, socket):
        teleport_id, byte_length = unpack_encrypted_varint(socket)

        self.teleport_id = teleport_id
        return self

    def get(self, item):
        return self.__dict__[item]