from Packets.PacketUtil import pack_varint
from Util import enforce_annotations

class OpenBook:
    @enforce_annotations
    def __init__(self, hand: int):
        hand = pack_varint(hand)

        self.hand = hand