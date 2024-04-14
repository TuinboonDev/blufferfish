from Packets.PacketUtil import Pack
from Util import enforce_annotations

from Packets.PacketUtil import Packet

Pack = Pack()

class LoginPlay(Packet):
    @enforce_annotations
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
            portal_cooldown
    ):
        return super().__init__(
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
            portal_cooldown
        )