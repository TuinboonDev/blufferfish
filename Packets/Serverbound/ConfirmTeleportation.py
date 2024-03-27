from Packets.PacketUtil import unpack_encrypted_varint

class ConfirmTeleportation:
    def create(self, socket):
        teleport_id = unpack_encrypted_varint(socket)

        self.teleport_id = teleport_id
        return self

    def get(self, item):
        return self.__dict__[item]