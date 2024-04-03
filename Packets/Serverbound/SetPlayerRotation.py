from Packets.PacketUtil import decrypt_byte

class SetPlayerRotation:
    def create(self, remaining_packet_length, socket):
        yaw = decrypt_byte(socket.recv(4))
        pitch = decrypt_byte(socket.recv(4))

        on_ground = decrypt_byte(socket.recv(1))

        #print(bytes("SetPlayerRotation".encode("utf-8")), decrypt_byte(socket.recv(1024)))

        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground
        return self

    def get(self, item):
        return self.__dict__[item]