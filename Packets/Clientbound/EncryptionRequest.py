from Packets.PacketUtil import pack_varint, write_string, pack_data
from Encryption import Encryption

class EncryptionRequest:
    def __init__(self, server_id, public_key, verify_token):
        server_id = write_string(server_id)

        public_key = pack_data(public_key)

        verify_token = pack_data(verify_token)

        self.server_id = server_id
        self.public_key = public_key
        self.verify_token = verify_token