class PlayerAction:
    def create(self, bytebuf, decryptor):
        status = bytebuf.unpack_encrypted_varint(decryptor)[0]
        position = bytebuf.decrypt_byte(bytebuf.recv(8), decryptor)
        position_bits = ''.join(format(byte, '08b') for byte in position)
        position_x = int(position_bits[0:26], 2)
        position_z = int(position_bits[26:52], 2)
        position_y = int(position_bits[52:], 2)
        face = bytebuf.decrypt_byte(bytebuf.recv(1), decryptor)
        sequence_id = bytebuf.unpack_encrypted_varint(decryptor)[0]

        self.status = status
        self.position = position
        self.position_x = position_x
        self.position_z = position_z
        self.position_y = position_y
        self.face = face
        self.sequence_id = sequence_id
        return self

    def get(self, item):
        return self.__dict__[item]