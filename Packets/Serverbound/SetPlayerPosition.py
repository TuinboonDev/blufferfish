from Packets.PacketUtil import decrypt_byte

class SetPlayerPosition:
    def create(self, remaining_packet_length, socket):
        x = decrypt_byte(socket.recv(8))
        y = decrypt_byte(socket.recv(8))
        z = decrypt_byte(socket.recv(8))

        on_ground = decrypt_byte(socket.recv(1))

        print(remaining_packet_length)

        print(bytes("SetPlayerPosition".encode("utf-8")), decrypt_byte(socket.recv(1024)))

        self.x = x
        self.y = y
        self.z = z
        self.on_ground = on_ground
        return self

    def get(self, item):
        return self.__dict__[item]