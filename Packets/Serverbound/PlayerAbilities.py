class PlayerAbilities:
    def create(self, bytebuf, decryptor):
        flags = bytebuf.unpack_encrypted_varint(decryptor)[0]

        self.flags = flags
        return self

    def get(self, item):
        return self.__dict__[item]