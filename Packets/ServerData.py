import base64

class ServerData:
    def __init__(self, name, protocl, max, online, sample, description, icon, secureChat, previewsChat):
        self.data = {
            "version": {},
            "players": {
                "sample": []
            },
            "description": {}
        }

        self.data["version"]["name"] = name
        self.data["version"]["protocol"] = protocl

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
