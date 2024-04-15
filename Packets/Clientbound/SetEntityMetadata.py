from Packets.PacketUtil import Pack
from Util import enforce_annotations
import struct

from Packets.PacketUtil import Packet

Pack = Pack()

class SetEntityMetadata(Packet):
    @enforce_annotations
    def __init__(self, entity_id: int, entries: list):
        entity_id = Pack.pack_varint(entity_id)

        entry_data = b''
        for entry in entries:
            entry_data += struct.pack("B", entry["index"])
            entry_data += Pack.pack_varint(entry["value_type"])
            entry_data += entry["value"]

        packet = entity_id + entry_data + b'\xff'

        return super().__init__(packet)