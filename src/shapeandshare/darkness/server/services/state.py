import logging

from pydantic import BaseModel

from ...sdk.contracts.dtos.sdk.requests.island.create import IslandCreateRequest
from ...sdk.contracts.dtos.sdk.requests.island.delete import IslandDeleteRequest
from ...sdk.contracts.dtos.sdk.requests.island.get import IslandGetRequest
from ...sdk.contracts.dtos.sdk.requests.world.create import WorldCreateRequest
from ...sdk.contracts.dtos.sdk.requests.world.delete import WorldDeleteRequest
from ...sdk.contracts.dtos.sdk.requests.world.get import WorldGetRequest
from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.dtos.tiles.island import Island
from ...sdk.contracts.dtos.tiles.tile import Tile
from ...sdk.contracts.dtos.tiles.world import World
from ..dao.island import IslandDao
from ..dao.tile import TileDao
from ..dao.world import WorldDao
from ..factories.entity.entity import EntityFactory
from ..factories.island.flat import FlatIslandFactory
from ..factories.world.world import WorldFactory

logger = logging.getLogger()


class StateService(BaseModel):
    worlddao: WorldDao
    islanddao: IslandDao
    tiledao: TileDao
    world_factory: WorldFactory
    entity_factory: EntityFactory
    flatisland_factory: FlatIslandFactory

    ### World ##################################

    async def world_create(self, request: WorldCreateRequest) -> str:
        logger.debug("[StateService] creating world")
        return await self.world_factory.create(name=request.name)

    async def world_lite_get(self, request: WorldGetRequest) -> World:
        return (await self.worlddao.get(world_id=request.id)).data

    async def world_get(self, request: WorldGetRequest) -> World:
        # Build a complete World from Lite objects
        world_lite: World = (await self.worlddao.get(world_id=request.id)).data
        island_ids: set[str] = world_lite.ids
        partial_world = world_lite.model_dump(exclude={"island_ids"})
        world: World = World.model_validate(partial_world)
        for island_id in island_ids:
            local_island: Island = await self.island_get(request=IslandGetRequest(world_id=request.id, island_id=island_id))
            world.contents[island_id] = local_island
        return world

    async def world_delete(self, request: WorldDeleteRequest) -> None:
        logger.debug("[StateService] deleting world")
        await self.worlddao.delete(world_id=request.id)

    ### Island ##################################

    async def island_create(self, request: IslandCreateRequest) -> str:
        logger.debug("[StateService] creating island")
        new_island: Island = await self.flatisland_factory.create(world_id=request.world_id, name=request.name, dimensions=request.dimensions, biome=request.biome)

        # Entity Factory Terrain Creation
        await self.entity_factory.terrain_generate(world_id=request.world_id, island=new_island)
        new_island: Island = (await self.islanddao.get(world_id=request.world_id, island_id=new_island.id)).data

        # Entity Factory Quantum
        await self.entity_factory.quantum(world_id=request.world_id, island=new_island)

        # add new island to world
        # add island to world and store

        # get
        wrapped_world_lite: WrappedData[World] = await self.worlddao.get(world_id=request.world_id)

        # update our state
        wrapped_world_lite.data.ids.add(new_island.id)

        # put
        await self.worlddao.put(wrapped_world=wrapped_world_lite)

        return new_island.id

    async def island_delete(self, request: IslandDeleteRequest) -> None:
        msg: str = f"[WorldService] deleting island {id}"
        logger.debug(msg)
        await self.islanddao.delete(world_id=request.world_id, island_id=request.island_id)

    async def island_lite_get(self, request: IslandGetRequest) -> Island:
        return (await self.islanddao.get(world_id=request.world_id, island_id=request.island_id)).data

    async def island_get(self, request: IslandGetRequest) -> Island:
        # Builds a complete Island from Lite objects
        island_lite: Island = (await self.islanddao.get(world_id=request.world_id, island_id=request.island_id)).data
        tile_ids: set[str] = island_lite.ids
        island_partial = island_lite.model_dump(exclude={"tile_ids"})
        # island: IslandFull = IslandFull.model_validate(island_partial)
        island: Island = Island.model_validate(island_partial)

        # re-hydrate the tiles
        for tile_id in tile_ids:
            tile: Tile = (await self.tiledao.get(world_id=request.world_id, island_id=island.id, tile_id=tile_id)).data
            island.contents[tile_id] = tile

        return island
