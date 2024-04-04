class ServerboundPluginMessage:
    def create(self, bytebuf, decryptor):
        identifier_length, byte_length = bytebuf.unpack_encrypted_varint(decryptor)
        identifier = ""
        for i in range(identifier_length):
            identifier += bytebuf.decrypt_byte(bytebuf.recv(1), decryptor).decode('utf-8')

        data_length = len(bytebuf)
        data = b''
        for i in range(data_length):
            data += bytebuf.decrypt_byte(bytebuf.recv(1), decryptor) #bit array

        self.identifier = identifier
        self.data = data
        return self

    def get(self, item):
        return self.__dict__[item]