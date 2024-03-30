from Packets.PacketUtil import pack_varint, write_string

class PlayerInfoUpdate:
    def __init__(self, actions, player_actions, properties):
        number_of_players = pack_varint(len(player_actions))

        players_field = b''

        for action in actions:
            if action == 0x01:
                for player in player_actions:
                    players_field += player["uuid"]
                    players_field += write_string(player["name"])
                    players_field += pack_varint(1)
                    players_field += write_string(properties["name"])
                    players_field += write_string(properties["value"])
                    players_field += int(properties["is_signed"]).to_bytes(1, byteorder='big', signed=True)
                    players_field += write_string(properties["signature"])
                    break

            if action == 0x08:
                players_field += int(player["show"]).to_bytes(1, byteorder='big', signed=True)

        actions = actions[0] | actions[1]

        actions = actions.to_bytes(1, byteorder='big', signed=True)

        self.actions = actions
        self.number_of_players = number_of_players
        self.players_field = players_field