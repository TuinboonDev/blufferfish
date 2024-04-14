from Packets.PacketUtil import Pack
from Util import enforce_annotations
import struct

from Packets.PacketUtil import Packet

Pack = Pack()

@enforce_annotations
def write_single_valued_paletted_container(entry: int):
    data = b''
    data += struct.pack('b', 0) # bits per entry
    data += Pack.pack_varint(entry)
    data += struct.pack('b', 0) # data array length

    return data


def write_data_ig():
    data = b''
    switch = 1
    for _ in range(24):
        data += struct.pack('h', 4096)
        data += write_single_valued_paletted_container(switch) #block palette
        data += write_single_valued_paletted_container(0) #bioma palette
        if switch == 1:
            switch = 9
        elif switch == 9:
            switch = 1

    return data

class ChunkDataUpdateLight(Packet):
    @enforce_annotations
    def __init__(self, chunk_x: int, chunk_z: int, data, block_entities: bytes):
        chunk_x = chunk_x.to_bytes(4, byteorder='big', signed=True)
        chunk_z = chunk_z.to_bytes(4, byteorder='big', signed=True)

        heightmaps = b'\x0A' + b'\x00' #idk what to do with this

        data = Pack.pack_data(write_data_ig())

        empty = Pack.pack_data(b'') #empty data because I dont know how to write real data

        block_entities = Pack.pack_data(block_entities) #block entities (which is also empty)

        stupid_bitsets = b'\x01\x00\x00\x00\x00\x00\x00\x00\x00'

        packet = (chunk_x
        + chunk_z
        + heightmaps
        + data
        + block_entities
        + stupid_bitsets
        + stupid_bitsets
        + stupid_bitsets
        + stupid_bitsets
        + empty
        + empty)

        return super().__init__(packet)