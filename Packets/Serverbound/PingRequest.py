class PingRequest:
    def create(self, bytebuf, decryptor):
        time = bytebuf.recv(8)

        self.time = time

        return self

    def get(self, item):
        return self.__dict__[item]