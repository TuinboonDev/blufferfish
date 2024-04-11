from Packets.PacketUtil import pack_data, write_string
from Util import enforce_annotations

class LoginSuccess:
    @enforce_annotations
    def __init__(self, uuid: bytes, username: str, properties: bytes):
        username = write_string(username)

        properties = pack_data(properties)

        self.uuid = uuid
        self.username = username
        self.properties = properties