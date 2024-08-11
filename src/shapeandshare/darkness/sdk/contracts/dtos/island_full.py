from ..types.tile import TileType
from .tiles.abtract import AbstractTile
from .tiles.tile import Tile


class IslandFull(AbstractTile[str, Tile]):
    tile_type: TileType = TileType.ISLAND
    dimensions: tuple[int, int] | None = None
    biome: TileType | None = None
