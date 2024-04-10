from Packets.PacketUtil import pack_varint

class AcknowledgeBlockChange:
    def __init__(self, sequence_id):
        sequence_id = pack_varint(sequence_id)

        self.sequence_id = sequence_id