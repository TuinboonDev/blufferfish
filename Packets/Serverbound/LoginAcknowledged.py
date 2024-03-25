import struct
from Packets.PacketUtil import unpack_varint

class LoginAcknowledged:
    def create(self, socket):

        return self

    def get(self, item):
        return self.__dict__[item]