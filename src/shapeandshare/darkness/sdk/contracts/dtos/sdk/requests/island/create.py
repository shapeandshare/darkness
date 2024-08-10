from pydantic import BaseModel

from .....types.tile import TileType


class IslandCreateRequest(BaseModel):
    world_id: str | None = None

    name: str | None = None
    dimensions: tuple[int, int]
    biome: TileType
