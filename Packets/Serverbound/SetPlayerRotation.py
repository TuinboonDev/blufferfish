class SetPlayerRotation:
    def create(self, bytebuf, decryptor):
        yaw = bytebuf.decrypt_byte(bytebuf.recv(4), decryptor)
        pitch = bytebuf.decrypt_byte(bytebuf.recv(4), decryptor)

        on_ground = bytebuf.decrypt_byte(bytebuf.recv(1), decryptor)

        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground
        return self

    def get(self, item):
        return self.__dict__[item]