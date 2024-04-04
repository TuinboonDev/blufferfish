from Packets.PacketUtil import pack_data, write_string, pack_varint
import struct

def encode_gamemode(gamemode):
    if gamemode == None:
        return int(-1).to_bytes(1, "big", signed=True)
    elif gamemode == "survival":
        return int(0).to_bytes(1, "big")
    elif gamemode == "creative":
        return int(1).to_bytes(1, "big")
    elif gamemode == "adventure":
        return int(2).to_bytes(1, "big")
    elif gamemode == "spectator":
        return int(3).to_bytes(1, "big")

class LoginPlay:
    def __init__(
            self,
            entity_id,
            is_hardcore,
            dimensions,
            max_players,
            view_distance,
            simulation_distance,
            reduced_debug_info,
            respawn_screen,
            limited_crafting,
            dimension_type,
            dimension_name,
            seed,
            gamemode,
            previous_gamemode,
            is_debug,
            is_flat,
            has_death_location,
            death_dimension,
            death_location,
            portal_cooldown
    ):

        entity_id = entity_id.to_bytes(4, "big", signed=True)
        is_hardcore = int(is_hardcore).to_bytes(1, "big")
        dimensions = pack_data(dimensions)
        max_players = pack_varint(max_players)
        view_distance = pack_varint(view_distance)
        simulation_distance = pack_varint(simulation_distance)
        reduced_debug_info = int(reduced_debug_info).to_bytes(1, "big")
        respawn_screen = int(respawn_screen).to_bytes(1, "big")
        limited_crafting = int(limited_crafting).to_bytes(1, "big")
        dimension_type = write_string(dimension_type)
        dimension_name = write_string(dimension_name)
        seed = struct.pack(">q", seed)
        gamemode = encode_gamemode(gamemode)
        previous_gamemode = encode_gamemode(previous_gamemode)
        is_debug = int(is_debug).to_bytes(1, "big")
        is_flat = int(is_flat).to_bytes(1, "big")

        do_death_location = has_death_location

        has_death_location = int(has_death_location).to_bytes(1, "big")
        if do_death_location:
            death_dimension = write_string(death_dimension)
            death_location = pack_data(death_location)
        portal_cooldown = pack_varint(portal_cooldown)

        self.entity_id = entity_id
        self.is_hardcore = is_hardcore
        self.dimensions = dimensions
        self.max_players = max_players
        self.view_distance = view_distance
        self.simulation_distance = simulation_distance
        self.reduced_debug_info = reduced_debug_info
        self.respawn_screen = respawn_screen
        self.limited_crafting = limited_crafting
        self.dimension_type = dimension_type
        self.dimension_name = dimension_name
        self.seed = seed
        self.gamemode = gamemode
        self.previous_gamemode = previous_gamemode
        self.is_debug = is_debug
        self.is_flat = is_flat
        self.has_death_location = has_death_location
        if do_death_location:
            self.death_dimension = death_dimension
            self.death_location = death_location
        self.portal_cooldown = portal_cooldown

