from pydantic import BaseModel

from ...types.tile import TileType


class IslandCreateRequest(BaseModel):
    dim: tuple[int, int]
    biome: TileType
