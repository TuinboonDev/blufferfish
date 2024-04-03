from Packets.PacketUtil import decrypt_byte, unpack_encrypted_varint

class PlayerSession:
    #TODO: Please fix
    def create(self, remaining_packet_length, socket):
        session_id = decrypt_byte(socket.recv(16))
        expires_at = decrypt_byte(socket.recv(8))
        public_key_length = unpack_encrypted_varint(socket)[0]
        public_key = socket.recv(public_key_length)
        key_signature_length = unpack_encrypted_varint(socket)[0]
        key_signature = socket.recv(key_signature_length)

        print(bytes("PlayerSession".encode("utf-8")), decrypt_byte(socket.recv(1024)))
        self.session_id = session_id
        self.expires_at = expires_at
        self.public_key = public_key
        self.key_signature = key_signature
        return self

    def get(self, item):
        return self.__dict__[item]