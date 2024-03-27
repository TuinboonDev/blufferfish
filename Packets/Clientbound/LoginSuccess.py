from Packets.PacketUtil import pack_data, write_string, pack_varint

class LoginSuccess:
    def __init__(self, uuid, username, properties):
        username = write_string(username)

        properties = pack_data(properties)

        self.uuid = uuid
        self.username = username
        self.properties = properties