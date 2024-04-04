class SetPlayerOnGround:
    def create(self, bytebuf, decryptor):
        on_ground = bytebuf.decrypt_byte(bytebuf.recv(1), decryptor)

        #TODO:

        self.on_ground = on_ground
        return self

    def get(self, item):
        return self.__dict__[item]