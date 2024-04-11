from Util import enforce_annotations

import struct

class GameEvent:
    @enforce_annotations
    def __init__(self, event: int, value: int):
        event = struct.pack('>B', event)
        value = struct.pack('f', value)

        self.event = event
        self.value = value