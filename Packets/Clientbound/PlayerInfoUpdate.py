from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

#TODO:
#TODO:
#TODO:

class PlayerInfoUpdate(Packet):
    @enforce_annotations
    def __init__(self, actions: list, player_actions: list, properties: dict):
        number_of_players = Pack.pack_varint(len(player_actions))

        players_field = b''

        for action in actions:
            if action == 0x01:
                for player in player_actions:
                    players_field += player["uuid"]
                    players_field += Pack.write_string(player["name"])
                    players_field += Pack.pack_varint(1)
                    players_field += Pack.write_string(properties["name"])
                    players_field += Pack.write_string(properties["value"])
                    players_field += int(properties["is_signed"]).to_bytes(1, byteorder='big', signed=True)
                    players_field += Pack.write_string(properties["signature"])
                    break

            if action == 0x08:
                players_field += int(player["show"]).to_bytes(1, byteorder='big', signed=True)

        actions = actions[0] | actions[1]

        actions = actions.to_bytes(1, byteorder='big', signed=True)

        packet = actions + player_actions + properties

        return super().__init__(packet)