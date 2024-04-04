from Packets.PacketUtil import pack_varint
import struct

class SetEntityMetadata:
    def __init__(self, entity_id, index, value_type, value):
        entity_id = pack_varint(entity_id)
        index = struct.pack("B", index)
        value_type = pack_varint(value_type)

        self.entity_id = entity_id
        self.index = index
        self.type = value_type
        self.value = value
        self.end_byte = b"\xff" #end byte somehow