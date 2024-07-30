from pydantic import BaseModel

from .tile import Tile


class Island(BaseModel):
    id: str
    name: str
    rbac: dict = {}
    tiles: dict[str, Tile] = {}
    dim: tuple[int, int] | None = None
