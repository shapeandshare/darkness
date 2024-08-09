from pydantic import BaseModel

from .....types.tile import TileType


class IslandCreateRequest(BaseModel):
    world_id: str
    name: str | None
    dimensions: tuple[int, int]
    biome: TileType
