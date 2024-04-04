class PlayerCommand:
    def create(self, bytebuf, decryptor):
        entity_id = bytebuf.unpack_encrypted_varint(decryptor)[0]
        action_id = bytebuf.unpack_encrypted_varint(decryptor)[0]
        jump_boost = bytebuf.unpack_encrypted_varint(decryptor)[0]

        self.entity_id = entity_id
        self.action_id = action_id
        self.jump_boost = jump_boost
        return self

    def get(self, item):
        return self.__dict__[item]