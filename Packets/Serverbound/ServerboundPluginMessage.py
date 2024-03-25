from Packets.PacketUtil import unpack_encrypted_varint, decrypt_byte

class ServerboundPluginMessage:
    def create(self, socket):
        #print(socket.recv(1024))
        identifier_length = unpack_encrypted_varint(socket)
        identifier = ""
        for i in range(identifier_length):
            identifier += decrypt_byte(socket.recv(1)).decode('utf-8')

        """ 
        data_length = unpack_encrypted_varint(socket)
        data = b""
        for i in range(data_length):
            data += socket.recv(1)
        """

        data = decrypt_byte(socket.recv(1024))

        self.identifier = identifier
        self.data = data
        return self

    def get(self, item):
        return self.__dict__[item]