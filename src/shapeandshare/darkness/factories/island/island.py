from pydantic import BaseModel

from ...contracts.dtos.island import Island
from ...contracts.types.tile import TileType
from .flat import FlatIslandFactory
from .flatland import FlatLandFactory


class IslandFactory(BaseModel):
    @staticmethod
    def flat(dim: tuple[int, int], biome: TileType) -> Island:
        return FlatIslandFactory.flat(dim=dim, biome=biome)

    @staticmethod
    def flatland(dim: tuple[int, int], biome: TileType) -> Island:
        return FlatLandFactory.generate(dim=dim, biome=biome)
