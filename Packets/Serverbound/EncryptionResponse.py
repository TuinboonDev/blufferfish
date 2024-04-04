class EncryptionResponse:
    def create(self, bytebuf, decryptor):
        shared_secret_length, byte_length = bytebuf.unpack_varint()

        shared_secret = b""
        for i in range(shared_secret_length):
            shared_secret += bytebuf.recv(1)

        verify_token_length, byte_length = bytebuf.unpack_varint()
        verify_token = b""
        for i in range(verify_token_length):
            verify_token += bytebuf.recv(1)

        self.shared_secret = shared_secret
        self.verify_token = verify_token
        return self

    def get(self, item):
        return self.__dict__[item]