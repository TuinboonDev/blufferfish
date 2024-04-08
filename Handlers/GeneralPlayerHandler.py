class GeneralPlayerHandler:
    def __init__(self):
        self.players = []
        self.player_count = 0

    def add_player(self, name, uuid, properties, skin_parts, socket):
        self.players.append({"name": name, "uuid": uuid, "entity_id": self.player_count, "properties": properties, "skin_parts": skin_parts, "socket": socket, "position": (8,320,8), "rotation": (0,0)})
        self.player_count += 1

    def remove_player(self, socket):
        for player in self.players:
            if player["socket"] == socket:
                self.players.remove(player)
                self.player_count -= 1
                break

    def get_rotation(self, entity_id):
        for player in self.players:
            if player["entity_id"] == entity_id:
                return player["rotation"]
        return None

    def set_rotation(self, entity_id, rotation):
        for player in self.players:
            if player["entity_id"] == entity_id:
                player["rotation"] = rotation
                break

    def get_position(self, entity_id):
        for player in self.players:
            if player["entity_id"] == entity_id:
                return player["position"]
        return None

    def set_position(self, entity_id, position):
        for player in self.players:
            if player["entity_id"] == entity_id:
                player["position"] = position
                break

    def get_online_players(self):
        return self.players

    def get_player_count(self):
        return self.player_count

    def get_all_other_players(self, name):
        players = []
        for player in self.players:
            if player["name"] != name:
                players.append(player)
        return players

    def get_entity_id(self, uuid):
        for player in self.players:
            if player["uuid"] == uuid:
                return player["entity_id"]
        return None