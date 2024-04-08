import struct
from Packets.PacketUtil import pack_data, pack_varint

def write_single_valued_paletted_container(entry):
    data = b''
    data += struct.pack('b', 0) # bits per entry
    data += pack_varint(entry)
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

class ChunkDataUpdateLight:
    def __init__(self, chunk_x, chunk_z, data, block_entities): #the data input is unused because I can
        chunk_x = chunk_x.to_bytes(4, byteorder='big', signed=True)
        chunk_z = chunk_z.to_bytes(4, byteorder='big', signed=True)

        heightmaps = b'\x0A' + b'\x00' #idk what to do with this

        data = pack_data(write_data_ig())

        empty = pack_data(b'') #empty data because I dont know how to write real data

        block_entities = pack_data(block_entities) #block entities (which is also empty)

        stupid_bitsets = b'\x01\x00\x00\x00\x00\x00\x00\x00\x00' #just another empty bitset because im stupid

        self.x = chunk_x
        self.z = chunk_z
        self.heightmaps = heightmaps
        self.data = data
        self.block_entities = block_entities
        self.sky_light_mask = stupid_bitsets
        self.block_light_mask = stupid_bitsets
        self.empty_sky_light_mask = stupid_bitsets
        self.empty_block_light_mask = stupid_bitsets
        self.sky_light_array_count = empty
        self.block_light_array_count = empty
