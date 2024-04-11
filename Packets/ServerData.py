from Util import enforce_annotations

import base64

class ServerData:
    @enforce_annotations
    def __init__(self, name: str, protocol: int, max: int, online: int, sample: list, description: str, icon: str, secureChat: bool, previewsChat: bool):
        self.data = {
            "version": {},
            "players": {
                "sample": []
            },
            "description": {}
        }

        self.data["version"]["name"] = name
        self.data["version"]["protocol"] = protocol

        self.data["players"]["max"] = max
        self.data["players"]["online"] = online
        self.data["players"]["sample"] = sample

        self.data["description"]["text"] = description

        with open(icon, "rb") as f:
            encoded = base64.b64encode(f.read())

        self.data["favicon"] = f"data:image/png;base64,{encoded.decode('utf-8')}"

        self.data["enforcesSecureChat"] = secureChat

        self.data["previewsChat"] = previewsChat

    def get_data(self):
        return self.data

    #TODO: Implement set_data method
    """
    def set_data(self, keys, values):
        self.data[keys] = values
    """
