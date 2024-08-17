from ...types.tile import TileType
from .abtract import AbstractTile
from .tile import Tile


class Chunk(AbstractTile[str, Tile]):
    tile_type: TileType = TileType.CHUNK
    dimensions: tuple[int, int] | None = None
    biome: TileType | None = None
    origin: str | None = None  # what is tile id at (0,0) of the nXm dim land
