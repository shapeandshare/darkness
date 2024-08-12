from ...types.tile import TileType
from .abtract import AbstractTile
from .tile import Tile


class Island(AbstractTile[str, Tile]):
    tile_type: TileType = TileType.ISLAND
    dimensions: tuple[int, int] | None = None
    biome: TileType | None = None
