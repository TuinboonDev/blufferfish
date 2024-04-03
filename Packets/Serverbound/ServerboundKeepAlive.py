from Packets.PacketUtil import decrypt_byte

class ServerboundKeepAlive:
    def create(self, remaining_packet_length, socket):
        keep_alive_id = decrypt_byte(socket.recv(8))

        self.keep_alive_id = keep_alive_id
        return self

    def get(self, item):
        return self.__dict__[item]