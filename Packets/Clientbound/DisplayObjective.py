from Packets.PacketUtil import pack_varint, write_string

class DisplayObjective:
    def __init__(self, position, score_name):
        position = pack_varint(position)
        score_name = write_string(score_name)

        self.position = position
        self.score_name = score_name