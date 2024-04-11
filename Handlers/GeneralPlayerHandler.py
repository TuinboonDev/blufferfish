import json
import socket
from Util import enforce_annotations

class Player:
    @enforce_annotations
    def __init__(self, name: str, uuid: bytes, entity_id: int, session: json, skin_parts: bytes, socket: socket.socket):
        self.name = name
        self.uuid = uuid
        self.entity_id = entity_id
        self.session = session
        self.skin_parts = skin_parts
        self.socket = socket
        self.position = (8,320,8)
        self.rotation = (0,0)

class GeneralPlayerHandler:
    def __init__(self):
        self.players = []
        self.player_count = 0

    @enforce_annotations
    def add_player(self, name: str, uuid: bytes, session: json, skin_parts: bytes, socket: socket.socket):
        player = Player(
            name,
            uuid,
            self.player_count,
            session,
            skin_parts,
            socket
        )
        self.players.append(player)
        self.player_count += 1

    @enforce_annotations
    def remove_player(self, socket: socket.socket):
        for player in self.players:
            if player.socket == socket:
                self.players.remove(player)
                self.player_count -= 1
                break

    @enforce_annotations
    def get_rotation(self, entity_id: int):
        for player in self.players:
            if player.entity_id == entity_id:
                return player.rotation
        return None

    @enforce_annotations
    def set_rotation(self, entity_id: int, rotation: tuple):
        for player in self.players:
            if player.rotation == entity_id:
                player.rotation = rotation
                break

    @enforce_annotations
    def get_position(self, entity_id: int):
        for player in self.players:
            if player.entity_id == entity_id:
                return player.position
        return None

    @enforce_annotations
    def set_position(self, entity_id: int, position: tuple):
        for player in self.players:
            if player.entity_id == entity_id:
                player.position = position
                break

    def get_online_players(self):
        return self.players

    def get_player_count(self):
        return self.player_count

    @enforce_annotations
    def get_all_other_players(self, name: str):
        return [player for player in self.players if player.name != name]

    @enforce_annotations
    def get_entity_id(self, uuid: bytes):
        for player in self.players:
            if player.uuid == uuid:
                return player.entity_id
        return None