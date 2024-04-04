import struct

class KeepAlive:
    def __init__(self, keep_alive_id):
        keep_alive_id = struct.pack(">q", keep_alive_id)

        self.keep_alive_id = keep_alive_id