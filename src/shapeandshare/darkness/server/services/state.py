import logging

from pydantic import BaseModel

from ...sdk.contracts.dtos.island import Island
from ...sdk.contracts.dtos.island_lite import IslandLite
from ...sdk.contracts.dtos.sdk.requests.island.create import IslandCreateRequest
from ...sdk.contracts.dtos.sdk.requests.island.delete import IslandDeleteRequest
from ...sdk.contracts.dtos.sdk.requests.island.get import IslandGetRequest
from ...sdk.contracts.dtos.sdk.requests.world.create import WorldCreateRequest
from ...sdk.contracts.dtos.sdk.requests.world.delete import WorldDeleteRequest
from ...sdk.contracts.dtos.sdk.requests.world.get import WorldGetRequest
from ...sdk.contracts.dtos.tile import Tile
from ...sdk.contracts.dtos.world import World
from ...sdk.contracts.dtos.world_lite import WorldLite
from ..dao.island import IslandDao
from ..dao.tile import TileDao
from ..dao.world import WorldDao
from ..factories.island.flat import FlatIslandFactory
from ..factories.world.world import WorldFactory

logger = logging.getLogger()


class StateService(BaseModel):
    worlddao: WorldDao
    islanddao: IslandDao
    tiledao: TileDao

    worldfactory: WorldFactory | None = None
    flatislandfactory: FlatIslandFactory | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.worldfactory = WorldFactory(worlddao=self.worlddao)
        self.flatislandfactory = FlatIslandFactory(islanddao=self.islanddao, tiledao=self.tiledao)

    ### World ##################################

    def world_create(self, request: WorldCreateRequest) -> str:
        logger.debug("[StateService] creating world")
        return self.worldfactory.create(name=request.name)

    def world_lite_get(self, request: WorldGetRequest) -> WorldLite:
        return self.worlddao.get(world_id=request.id).data

    def world_get(self, request: WorldGetRequest) -> World:
        # logger.info("- 1 -----------------------------------------")

        # Build a complete World from Lite objects
        world_lite: WorldLite = self.worlddao.get(world_id=request.id).data
        island_ids: set[str] = world_lite.island_ids
        # logger.info(f"island_ids={island_ids}")
        partial_world = world_lite.model_dump(exclude={"island_ids"})
        # logger.info("- 2 -----------------------------------------")
        # logger.info(partial_world)
        world: World = World.model_validate(partial_world)
        # logger.info("- 3 -----------------------------------------")
        # logger.info(world)
        # logger.info("- 4 -----------------------------------------")
        for island_id in island_ids:
            local_island: Island = self.island_get(request=IslandGetRequest(world_id=request.id, island_id=island_id))
            world.islands[island_id] = local_island
        return world

    def world_delete(self, request: WorldDeleteRequest) -> None:
        logger.debug("[StateService] deleting world")
        self.worlddao.delete(world_id=request.id)

    ### Island ##################################

    def island_create(self, request: IslandCreateRequest) -> str:
        logger.debug("[StateService] creating island")
        new_island: IslandLite = self.flatislandfactory.create(
            world_id=request.world_id, name=request.name, dimensions=request.dimensions, biome=request.biome
        )
        # add new island to world
        # add island to world and store
        world_lite: WorldLite = self.worlddao.get(world_id=request.world_id).data
        world_lite.island_ids.add(new_island.id)
        self.worlddao.put(world=world_lite)

        return new_island.id

    def island_delete(self, request: IslandDeleteRequest) -> None:
        msg: str = f"[WorldService] deleting island {id}"
        logger.debug(msg)
        self.islanddao.delete(world_id=request.world_id, island_id=request.island_id)

    def island_lite_get(self, request: IslandGetRequest) -> IslandLite:
        return self.islanddao.get(world_id=request.world_id, island_id=request.island_id).data

    def island_get(self, request: IslandGetRequest) -> Island:
        # Builds a complete Island from Lite objects
        island_lite: IslandLite = self.islanddao.get(world_id=request.world_id, island_id=request.island_id).data
        tile_ids: set[str] = island_lite.tile_ids
        island_partial = island_lite.model_dump(exclude={"tile_ids"})
        island: Island = Island.model_validate(island_partial)

        # re-hydrate the tiles
        for tile_id in tile_ids:
            tile: Tile = self.tiledao.get(world_id=request.world_id, island_id=island.id, tile_id=tile_id).data
            island.tiles[tile_id] = tile

        return island
