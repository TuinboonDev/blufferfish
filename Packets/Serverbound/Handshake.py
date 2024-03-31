import struct
from Packets.PacketUtil import unpack_varint

class Handshake:
    def create(self, remaining_packet_length, socket):
        protocol_version, byte_length = unpack_varint(socket)
        server_address_length, byte_length = unpack_varint(socket)
        server_address = ""
        for i in range(server_address_length):
            server_address += socket.recv(1).decode("utf-8")
        server_port = struct.unpack('>H', socket.recv(2))[0]
        next_state = int.from_bytes(socket.recv(1), byteorder='big')

        self.protocol_version = protocol_version
        self.server_address_length = server_address_length
        self.server_address = server_address
        self.server_port = server_port
        self.next_state = next_state

        return self

    def get(self, item):
        return self.__dict__[item]