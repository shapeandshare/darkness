from pydantic import BaseModel

from ..types.tile import TileType


class IslandLite(BaseModel):
    id: str
    name: str
    rbac: dict = {}
    tile_ids: set[str] = set()
    dimensions: tuple[int, int] | None = None
    biome: TileType | None = None
