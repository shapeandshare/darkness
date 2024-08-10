from abc import abstractmethod

from pydantic import BaseModel

from ....sdk.contracts.types.tile import TileType
from ...dao.island import IslandDao


class AbstractIslandFactory(BaseModel):
    islanddao: IslandDao

    @abstractmethod
    async def create(self, world_id: str, name: str | None, dimensions: tuple[int, int], biome: TileType) -> str:
        pass
