from Packets.PacketUtil import pack_varint, write_string

class PlayerInfoUpdate:
    def __init__(self, actions, players_list):
        number_of_players = pack_varint(len(players_list))

        players = b''

        for player in players_list:
            players += player["uuid"]
            players += write_string(player["name"])
            players += pack_varint(0)

        self.actions = actions
        self.number_of_players = number_of_players
        self.players = players