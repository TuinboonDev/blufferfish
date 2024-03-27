from Packets.PacketUtil import pack_varint, pack_data

class ChunkDataUpdateLight:
    def __init__(self, chunk_x, chunk_z, data, block_entities):
        chunk_x = chunk_x.to_bytes(4, byteorder='big', signed=True)
        chunk_z = chunk_z.to_bytes(4, byteorder='big', signed=True)

        heightmaps = b'\x0A' + b'\x00'

        data = pack_data(data)

        block_entities = pack_data(block_entities)

        stupid_bitsets = b'\x01\x00\x00\x00\x00\x00\x00\x00\x00'

        self.x = chunk_x
        self.z = chunk_z
        self.heightmaps = heightmaps
        self.data = data
        self.block_entities = block_entities
        self.sky_light_mask = stupid_bitsets
        self.block_light_mask = stupid_bitsets
        self.empty_sky_light_mask = stupid_bitsets
        self.empty_block_light_mask = stupid_bitsets
        self.sky_light_array_count = data
        self.block_light_array_count = data
