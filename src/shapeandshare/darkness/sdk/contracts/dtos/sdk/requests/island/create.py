from pydantic import BaseModel

from .....types.tile import TileType


class IslandCreateRequest(BaseModel):
    dimensions: tuple[int, int]
    biome: TileType
