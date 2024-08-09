import logging
import uuid

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

logger = logging.getLogger()


class StateService(BaseModel):
    worlddao: WorldDao
    islanddao: IslandDao
    tiledao: TileDao

    flatislandfactory: FlatIslandFactory | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flatislandfactory = FlatIslandFactory(islanddao=self.islanddao, tiledao=self.tiledao)

    ### World ##################################

    def world_create(self, request: WorldCreateRequest) -> str:
        logger.debug("[StateService] creating world")
        new_world: WorldLite = WorldLite(id=str(uuid.uuid4()), name=request.name)
        self.worlddao.post(world=new_world)
        return new_world.id

    def world_lite_get(self, request: WorldGetRequest) -> WorldLite:
        return self.worlddao.get(world_id=request.id).data

    def world_get(self, request: WorldGetRequest) -> World:
        # Build a complete World from Lite objects
        world_lite: WorldLite = self.worlddao.get(world_id=request.id).data
        island_ids: set[str] = world_lite.island_ids
        partial_world = world_lite.model_dump(exclude={"island_ids"})
        world: World = World().model_load(partial_world)
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
        return new_island.id

    def island_delete(self, request: IslandDeleteRequest) -> None:
        msg: str = f"[WorldService] deleting island {id}"
        logger.debug(msg)
        self.islanddao.delete(world_id=request.world_id, island_id=request.island_id)

    def island_lite_get(self, request: IslandGetRequest) -> IslandLite:
        return self.islandao.get(world_id=request.world_id, island_id=request.island_id)

    def island_get(self, request: IslandGetRequest) -> Island:
        # Builds a complete Island from Lite objects
        island_lite: IslandLite = self.islandao.get(world_id=request.world_id, island_id=request.island_id)
        tile_ids: set[str] = island_lite.tile_ids
        island_partial = island_lite.model_dump(exclude={"tile_ids"})
        island: Island = Island.model_validate(island_partial)

        # re-hydrate the tiles
        for tile_id in tile_ids:
            tile: Tile = self.tiledao.get(world_id=request.world_id, island_id=island.id, tile_id=tile_id).data
            island.tiles[tile_id] = tile

        return island
