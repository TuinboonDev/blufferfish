class PlayerAbilities:
    def create(self, bytebuf, decryptor):
        flags = bytebuf.unpack_encrypted_varint()[0]

        self.flags = flags
        return self

    def get(self, item):
        return self.__dict__[item]