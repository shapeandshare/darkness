from pydantic import BaseModel

from ....sdk.contracts.dtos.island import Island
from ....sdk.contracts.types.tile import TileType
from .flat import FlatIslandFactory


class IslandFactory(BaseModel):
    @staticmethod
    def basic(dimensions: tuple[int, int], biome: TileType) -> Island:
        return FlatIslandFactory.generate(dimensions=dimensions, biome=biome)
