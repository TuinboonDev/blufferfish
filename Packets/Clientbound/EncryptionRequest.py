from Packets.PacketUtil import write_string, pack_data
from Util import enforce_annotations

class EncryptionRequest:
    @enforce_annotations
    def __init__(self, server_id: str, public_key: bytes, verify_token: bytes):
        server_id = write_string(server_id)

        public_key = pack_data(public_key)

        verify_token = pack_data(verify_token)

        self.server_id = server_id
        self.public_key = public_key
        self.verify_token = verify_token