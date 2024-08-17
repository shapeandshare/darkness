from pydantic import BaseModel

from .....types.tile import TileType


class ChunkCreateRequest(BaseModel):
    world_id: str | None = None

    name: str | None = None
    dimensions: tuple[int, int]
    biome: TileType
