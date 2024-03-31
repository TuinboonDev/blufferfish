from Packets.PacketUtil import unpack_encrypted_varint, decrypt_byte

class ServerboundPluginMessage:
    def create(self, remaining_packet_length, socket):
        identifier_length, byte_length = unpack_encrypted_varint(socket)
        identifier = ""
        for i in range(identifier_length):
            identifier += decrypt_byte(socket.recv(1)).decode('utf-8')

        data_length = remaining_packet_length - byte_length - identifier_length
        print(data_length)
        data = b''
        for i in range(data_length):
            data += decrypt_byte(socket.recv(1)) #bit array

        self.identifier = identifier
        self.data = data
        return self

    def get(self, item):
        return self.__dict__[item]