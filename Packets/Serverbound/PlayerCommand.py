from Packets.PacketUtil import decrypt_byte, unpack_encrypted_varint

class PlayerCommand:
    def create(self, remaining_packet_length, socket):
        entity_id = unpack_encrypted_varint(socket)
        action_id = unpack_encrypted_varint(socket)
        jump_boost = unpack_encrypted_varint(socket)

        self.entity_id = entity_id
        self.action_id = action_id
        self.jump_boost = jump_boost
        return self

    def get(self, item):
        return self.__dict__[item]