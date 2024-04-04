class SetPlayerPositionRotation:
    def create(self, bytebuf, decryptor):
        x = bytebuf.decrypt_byte(bytebuf.recv(8), decryptor)
        y = bytebuf.decrypt_byte(bytebuf.recv(8), decryptor)
        z = bytebuf.decrypt_byte(bytebuf.recv(8), decryptor)

        yaw = bytebuf.decrypt_byte(bytebuf.recv(4), decryptor)
        pitch = bytebuf.decrypt_byte(bytebuf.recv(4), decryptor)

        on_ground = bytebuf.decrypt_byte(bytebuf.recv(1), decryptor)

        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground
        return self

    def get(self, item):
        return self.__dict__[item]