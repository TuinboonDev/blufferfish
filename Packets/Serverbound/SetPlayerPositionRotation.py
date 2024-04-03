from Packets.PacketUtil import decrypt_byte

class SetPlayerPositionRotation:
    def create(self, remaining_packet_length, socket):
        x = decrypt_byte(socket.recv(8))
        y = decrypt_byte(socket.recv(8))
        z = decrypt_byte(socket.recv(8))

        yaw = decrypt_byte(socket.recv(4))
        pitch = decrypt_byte(socket.recv(4))

        on_ground = decrypt_byte(socket.recv(1))

        #print(bytes("SetPlayerPositionRotation".encode("utf-8")), decrypt_byte(socket.recv(1024)))

        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground
        return self

    def get(self, item):
        return self.__dict__[item]