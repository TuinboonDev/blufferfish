class ConfirmTeleportation:
    def create(self, bytebuf, decryptor):
        teleport_id, byte_length = bytebuf.unpack_encrypted_varint(decryptor)

        self.teleport_id = teleport_id
        return self

    def get(self, item):
        return self.__dict__[item]