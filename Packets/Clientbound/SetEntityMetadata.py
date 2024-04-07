from Packets.PacketUtil import pack_varint
import struct

class SetEntityMetadata:
    def __init__(self, entity_id, entries):
        entity_id = pack_varint(entity_id)

        entry_data = b''
        for entry in entries:
            entry_data += struct.pack("B", entry["index"])
            entry_data += pack_varint(entry["value_type"])
            entry_data += entry["value"]

        self.entity_id = entity_id
        self.entry_data = entry_data
        self.end_byte = b'\xff' #end byte somehow

        print(self.__dict__)