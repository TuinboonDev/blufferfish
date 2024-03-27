from Packets.PacketUtil import pack_varint

class OpenBook:
    def __init__(self, hand):
        hand = pack_varint(hand)

        self.hand = hand