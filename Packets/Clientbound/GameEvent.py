import struct

class GameEvent:
    def __init__(self, event, value):
        event = struct.pack(">B", event)
        value = struct.pack("f", value)

        self.event = event
        self.value = value