from Util import enforce_annotations

import struct

class KeepAlive:
    @enforce_annotations
    def __init__(self, keep_alive_id: int):
        keep_alive_id = struct.pack('>q', keep_alive_id)

        self.keep_alive_id = keep_alive_id