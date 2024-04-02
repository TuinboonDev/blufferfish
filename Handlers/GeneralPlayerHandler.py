class GeneralPlayerHandler:
    def __init__(self):
        self.players = []
        self.player_count = 0

    def add_player(self, name, uuid, properties):
        self.players.append({"name": name, "uuid": uuid, "entity_id": self.player_count, "properties": properties})
        self.player_count += 1

    def remove_player(self, uuid):
        for player in self.players:
            if player["uuid"] == uuid:
                self.players.remove(player)
                self.player_count -= 1
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