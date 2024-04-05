from Packets.PacketUtil import pack_varint

class SetHeadRotation:
    def __init__(self, entity_id, yaw):
        entity_id = pack_varint(entity_id)

        self.entity_id = entity_id
        self.yaw = yaw