import struct

class WorldEvent:
    def __init__(self, event_id, location, data, disable_relative_volume):
        event_id = struct.pack(">I", event_id)
        data = struct.pack(">I", data)
        disable_relative_volume = int(disable_relative_volume).to_bytes(1, byteorder="big")

        self.event_id = event_id
        self.location = location
        self.data = data
        self.disable_relative_volume = disable_relative_volume