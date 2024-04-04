class ServerboundKeepAlive:
    def create(self, bytebuf, decryptor):
        keep_alive_id = bytebuf.decrypt_byte(bytebuf.recv(8), decryptor)

        self.keep_alive_id = keep_alive_id
        return self

    def get(self, item):
        return self.__dict__[item]