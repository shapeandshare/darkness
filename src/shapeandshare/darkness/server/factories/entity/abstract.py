import asyncio
import logging
import uuid
from asyncio import Queue

from pydantic import BaseModel

from ....sdk.contracts.dtos.entities.entity import Entity
from ....sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ....sdk.contracts.dtos.tiles.tile import Tile
from ....sdk.contracts.errors.server.factory import FactoryError
from ....sdk.contracts.types.entity import EntityType
from ....sdk.contracts.types.tile import TileType
from ...dao.entity import EntityDao
from ...dao.tile import TileDao

logger = logging.getLogger()


class AbstractEntityFactory(BaseModel):
    entitydao: EntityDao
    tiledao: TileDao

    @staticmethod
    async def producer(ids: set[str], queue: Queue):
        for local_id in ids:
            await queue.put(local_id)

    async def generate(self, world_id: str, island_id: str, tile_id: str) -> None:
        # get entities ids for the tile
        local_tile: WrappedData[Tile] = await self.tiledao.get(tokens={"world_id": world_id, "island_id": island_id, "tile_id": tile_id})
        local_tile.data = Tile.model_validate(local_tile.data)
        if len(local_tile.data.ids) > 0:
            msg: str = f"entity generation can not occur on a tile with pre-existing entities, world_id: {world_id}, island_id: {island_id}, tile_id: {tile_id}"
            raise FactoryError(msg)

        # Review types now
        if local_tile.data.tile_type == TileType.GRASS:
            new_entity: Entity = Entity(id=str(uuid.uuid4()), entity_type=EntityType.GRASS)
            await self.entitydao.post(tokens={"world_id": world_id, "island_id": island_id, "tile_id": tile_id}, document=new_entity)
            local_tile.data.ids.add(new_entity.id)

        elif local_tile.data.tile_type == TileType.FOREST:
            new_entity: Entity = Entity(id=str(uuid.uuid4()), entity_type=EntityType.TREE)
            await self.entitydao.post(tokens={"world_id": world_id, "island_id": island_id, "tile_id": tile_id}, document=new_entity)
            local_tile.data.ids.add(new_entity.id)

        elif local_tile.data.tile_type == TileType.OCEAN:
            new_entity: Entity = Entity(id=str(uuid.uuid4()), entity_type=EntityType.FISH)
            await self.entitydao.post(tokens={"world_id": world_id, "island_id": island_id, "tile_id": tile_id}, document=new_entity)
            local_tile.data.ids.add(new_entity.id)

        await self.tiledao.put(tokens={"world_id": world_id, "island_id": island_id}, wrapped_document=local_tile)

    async def grow_entities(self, world_id: str, island_id: str, tile_id: str):
        # get entities ids for the tile
        local_tile: WrappedData[Tile] = await self.tiledao.get(tokens={"world_id": world_id, "island_id": island_id, "tile_id": tile_id})
        local_tile.data = Tile.model_validate(local_tile.data)

        async def entity_producer(queue: Queue):
            for entity_id in local_tile.data.ids:
                await queue.put(entity_id)

        async def step_one():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_entity_id: str = await queue.get()

                    # TODO: Process entity

                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(entity_producer(queue), consumer(queue))

        await step_one()

        # async def entity_producer(local_tile.data.ids)

        # entity_ids: set[str] = await self.entitydao.get_entities(world_id=world_id, island_id=island_id, tile_id=tile_id)

    # @abstractmethod
    # async def create(self, world_id: str, name: str | None, dimensions: tuple[int, int], biome: TileType) -> str:
    #     """ """
