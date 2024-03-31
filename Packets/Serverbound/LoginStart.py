from Packets.PacketUtil import unpack_varint

class LoginStart:
    def create(self, remaining_packet_length, socket):
        name_length, byte_length = unpack_varint(socket)
        name = ""
        for i in range(name_length):
            name += socket.recv(1).decode('utf-8')
        uuid_bytes = socket.recv(16)
        #uuid = ''.join('{:02x}'.format(x) for x in uuid_bytes)

        self.name_length = name_length
        self.name = name
        self.uuid_bytes = uuid_bytes
        return self

    def get(self, item):
        return self.__dict__[item]