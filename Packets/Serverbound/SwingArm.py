class SwingArm:
    def create(self, bytebuf, decryptor):
        hand = bytebuf.unpack_encrypted_varint(decryptor)[0]

        self.hand = hand
        return self

    def get(self, item):
        return self.__dict__[item]