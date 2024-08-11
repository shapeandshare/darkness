from ..types.tile import TileType
from .island_full import IslandFull
from .tiles.abtract import AbstractTile


class WorldFull(AbstractTile[str, IslandFull]):
    """Basic World"""

    tile_type: TileType = TileType.WORLD
