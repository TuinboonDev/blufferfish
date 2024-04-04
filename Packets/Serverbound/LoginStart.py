class LoginStart:
    def create(self, bytebuf, decryptor):
        name_length, byte_length = bytebuf.unpack_varint()
        name = ""
        for i in range(name_length):
            name += bytebuf.recv(1).decode('utf-8')
        uuid_bytes = bytebuf.recv(16)
        #uuid = ''.join('{:02x}'.format(x) for x in uuid_bytes)

        self.name_length = name_length
        self.name = name
        self.uuid_bytes = uuid_bytes
        return self

    def get(self, item):
        return self.__dict__[item]