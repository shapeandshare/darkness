from pydantic import BaseModel

from src.darkness.contracts.types.tile import TileType


class IslandCreateRequest(BaseModel):
    dim: tuple[int, int]
    biome: TileType
