import struct

class Handshake:
    def create(self, bytebuf, decryptor):
        protocol_version, byte_length = bytebuf.unpack_varint()
        server_address_length, byte_length = bytebuf.unpack_varint()
        server_address = ""
        for i in range(server_address_length):
            server_address += bytebuf.recv(1).decode("utf-8")
        server_port = struct.unpack('>H', bytebuf.recv(2))[0]
        next_state = int.from_bytes(bytebuf.recv(1), byteorder='big')

        self.protocol_version = protocol_version
        self.server_address_length = server_address_length
        self.server_address = server_address
        self.server_port = server_port
        self.next_state = next_state

        return self

    def get(self, item):
        return self.__dict__[item]