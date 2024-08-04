from pydantic import BaseModel

from ....sdk.contracts.dtos.island import Island
from ....sdk.contracts.types.tile import TileType
from .flat import FlatIslandFactory
from .flatland import FlatLandFactory


class IslandFactory(BaseModel):
    @staticmethod
    def flat(dimensions: tuple[int, int], biome: TileType) -> Island:
        return FlatIslandFactory.flat(dimensions=dimensions, biome=biome)

    @staticmethod
    def flatland(dimensions: tuple[int, int], biome: TileType) -> Island:
        return FlatLandFactory.generate(dimensions=dimensions, biome=biome)
