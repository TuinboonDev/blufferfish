from Util import enforce_annotations

class PingResponse:
    @enforce_annotations
    def __init__(self, time: bytes):
        self.time = time