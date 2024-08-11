from ..types.tile import TileType
from .island import Island
from .tiles.abtract import AbstractTile


class World(AbstractTile[str, Island]):
    """Basic World"""

    tile_type: TileType = TileType.WORLD
