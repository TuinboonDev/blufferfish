class PlayerSession:
    #TODO: Please fix
    def create(self, bytebuf, decryptor):
        session_id = bytebuf.decrypt_byte(bytebuf.recv(16), decryptor)
        expires_at = bytebuf.decrypt_byte(bytebuf.recv(8), decryptor)
        public_key_length = bytebuf.unpack_encrypted_varint(decryptor)[0]
        public_key = bytebuf.decrypt_byte(bytebuf.recv(public_key_length), decryptor)
        key_signature_length = bytebuf.unpack_encrypted_varint(decryptor)[0]
        key_signature = bytebuf.decrypt_byte(bytebuf.recv(key_signature_length), decryptor)

        self.session_id = session_id
        self.expires_at = expires_at
        self.public_key = public_key
        self.key_signature = key_signature
        return self

    def get(self, item):
        return self.__dict__[item]