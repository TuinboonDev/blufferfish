from Packets.PacketUtil import decrypt_byte

class SetPlayerOnGround:
    def create(self, remaining_packet_length, socket):
        on_ground = decrypt_byte(socket.recv(1))

        #TODO:

        self.on_ground = on_ground
        return self

    def get(self, item):
        return self.__dict__[item]