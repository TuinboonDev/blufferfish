from Packets.PacketUtil import pack_varint, write_string
from Util import enforce_annotations

class DisplayObjective:
    @enforce_annotations
    def __init__(self, position: bytes, score_name: str):
        position = pack_varint(position)
        score_name = write_string(score_name)

        self.position = position
        self.score_name = score_name