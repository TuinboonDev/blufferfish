from Packets.PacketUtil import unpack_varint

class EncryptionResponse:
    def create(self, socket):
        shared_secret_length = unpack_varint(socket)

        shared_secret = b""
        for i in range(shared_secret_length):
            shared_secret += socket.recv(1)

        verify_token_length = unpack_varint(socket)
        verify_token = b""
        for i in range(verify_token_length):
            verify_token += socket.recv(1)

        self.shared_secret = shared_secret
        self.verify_token = verify_token
        return self

    def get(self, item):
        return self.__dict__[item]