from Packets.PacketUtil import Pack
from Util import enforce_annotations
from Handlers.GeneralChunkHandler import generate_chunk, generate_noise

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

noise = generate_noise(1024, 1024, seed=12345)

class ChunkDataUpdateLight(Packet):
    @enforce_annotations
    def __init__(self, chunk_x: int, chunk_z: int, data: bytes, block_entities: bytes):
        data = Pack.pack_data(generate_chunk(noise, chunk_x, chunk_z).serialize())

        chunk_x = chunk_x.to_bytes(4, byteorder='big', signed=True)
        chunk_z = chunk_z.to_bytes(4, byteorder='big', signed=True)

        heightmaps = b'\x0A\x00' #idk what to do with this


        empty = b'\x00' #empty data because I dont know how to write real data

        block_entities = b'\x00' #block entities (which is also empty)

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