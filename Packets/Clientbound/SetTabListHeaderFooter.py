from Packets.PacketUtil import Pack
from Util import enforce_annotations

import struct

Pack = Pack()

class SetTabListHeaderFooter:
    @enforce_annotations
    def __init__(self, header: str, footer: str):
        tag_compound = b'\x0A'
        name_compound_length = struct.pack('>H', len("compound"))
        name_compound = Pack.write_string("compound")
        tag_string = b'\x08'
        key_length = struct.pack('>H', len("text"))
        key = Pack.write_string("text")
        header_length = struct.pack('>H', len(header))
        header = Pack.write_string(header)
        footer_length = struct.pack('>H', len(footer))
        footer = Pack.write_string(footer)
        end = b'\x00'

        print(footer_length)

        data = (
            #tag_compound +
            #name_compound_length +
            #name_compound +


            tag_string +
            key_length +
            key +

            header_length +
            header +



            tag_string +
            key_length +
            key +

            footer_length +
            footer +

            end
                )

        self.data = data