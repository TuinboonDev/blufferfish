from Packets.PacketUtil import pack_varint

class BlockUpdate:
    def __init__(self, location, block_id):
        block_id = pack_varint(block_id)

        self.location = location
        self.block_id = block_id
