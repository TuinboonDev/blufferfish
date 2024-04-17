"""
Make an api to abstract away chunk logic. This includes:
creating a classes for chunks, chunk sections, and perhaps an enum for blocks (although not necessary)
making methods for serializing them (you'll have to read into the relevant wiki page, be sure to ask questions)
(optional) adding convenience methods for setting and getting blocks (will be useful for when you'll be implementing player block interactions)
Sample perlin noise at all (x, z) positions. Remember that at integer coordinates the noise value is always the same. You'll have to transform block coordinates somehow.
Fill with blocks to noise height
Adjust noise until looks good
"""
import random
import math
import struct

from Packets.PacketUtil import Pack
from Util import enforce_annotations

Pack = Pack()

class Block:
    def __init__(self, block_id: int):
        self.block_id = block_id

class ChunkSection:
    def __init__(self, blocks: list[Block]):
        self.blocks = blocks

    def get_blocks(self):
        return [block.block_id for block in self.blocks]
    
    def serialize(self) -> bytes:
        data = b''
        data += struct.pack('>h', 4096)
        unique_blocks = list(set(self.get_blocks()))
        bpe = math.ceil(math.log2(len(unique_blocks)))
        if bpe > 0 and bpe < 4: bpe = 4
        if bpe > 8: bpe = 15

        palette = b''

        # Single valued
        if bpe == 0:
            palette += struct.pack('B', bpe)
            palette += Pack.pack_varint(unique_blocks[0]) #Should be the only block in the array
            palette += Pack.pack_varint(0)

        # Indirect
        elif bpe in range(4, 9):
            palette += struct.pack('B', bpe)
            palette += Pack.pack_varint(len(unique_blocks))
            for block in unique_blocks:
                palette += Pack.pack_varint(block)
            blocks_per_long = 64 // bpe
            data_length = 4096 // blocks_per_long
            print(data_length)
            palette += Pack.pack_varint(data_length)
            data_array: list[int] = [0 for _ in range(data_length)]
            for i in range(4096):
                data_array[i // blocks_per_long] |= unique_blocks.index(self.get_blocks()[i]) << bpe * (i % blocks_per_long)
            for data_item in data_array:
                palette += struct.pack('Q', data_item)

        # Direct
        elif bpe == 15:
            #TODO: Implement direct
            print("Direct")

        else:
            raise ValueError(f"Invalid bpe {bpe}")

        data += palette

        #Biome palette
        data += struct.pack('b', 0)
        data += Pack.pack_varint(0)
        data += struct.pack('b', 0)
        #-------------------

        return data

class Chunk:
    def __init__(self, chunk_sections: list[ChunkSection]):
        self.chunk_sections = chunk_sections

    def serialize(self):
        data = b''
        for section in self.chunk_sections:
            data += section.serialize()
        return data

    def get_sections(self):
        return self.chunk_sections

def generate_chunk(noise: list, chunk_x: int, chunk_z: int) -> Chunk:
    chunk_sections = []
    for chunk_section in range(24):
        blocks = []
        for y in range(16):
            for z in range(16):
                for x in range(16):
                    block_y = -64 + (chunk_section * 16) + y
                    y_noise = 96 + get_noise(noise, chunk_x * 16 + x, chunk_z * 16 + z) * 128
                    if block_y < y_noise:
                        blocks.append(Block(1))
                    else:
                        blocks.append(Block(0))
        chunk_sections.append(ChunkSection(blocks))

    return Chunk(chunk_sections)

def get_noise(noise: list[list[float]], x: int, z: int) -> float:
    return noise[x][z]

def generate_noise(width: int, height: int, seed: int) -> list[list[float]]:
    l1 = []
    for x in range(width):
        l2 = []
        for z in range(height):
            l2.append(math.sin(x / 10) * math.sin(z / 10) / 10)
        l1.append(l2)

    return l1

noise = generate_noise(1024, 1024, seed=12345)

def realchunk(chunk_x: int, chunk_z: int):
    return generate_chunk(noise, chunk_x, chunk_z).serialize()


"""@enforce_annotations
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

    return data"""
