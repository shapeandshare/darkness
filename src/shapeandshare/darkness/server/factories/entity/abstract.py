import asyncio
import logging
import uuid
from asyncio import Queue

from pydantic import BaseModel

from ....sdk.contracts.dtos.entities.entity import Entity
from ....sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ....sdk.contracts.dtos.tiles.address import Address
from ....sdk.contracts.dtos.tiles.tile import Tile
from ....sdk.contracts.errors.server.factory import FactoryError
from ....sdk.contracts.types.entity import EntityType
from ....sdk.contracts.types.tile import TileType
from ...services.dao import DaoService

logger = logging.getLogger()


class AbstractEntityFactory(BaseModel):
    # entitydao: TileDao[Entity]
    # tiledao: TileDao[Tile]
    daoservice: DaoService

    @staticmethod
    async def producer(ids: set[str], queue: Queue):
        for local_id in ids:
            await queue.put(local_id)

    async def generate(self, address: Address) -> None:
        # get entities ids for the tile
        local_tile: WrappedData[Tile] = await self.daoservice.get(address=address)
        if len(local_tile.data.ids) > 0:
            msg: str = f"entity generation can not occur on a tile with pre-existing entities, {address}"
            raise FactoryError(msg)

        # Review types now
        if local_tile.data.tile_type == TileType.GRASS:
            new_entity: Entity = Entity(id=str(uuid.uuid4()), entity_type=EntityType.GRASS)
            address_entity: Address = Address.model_validate({**address.model_dump(), "entity_id": new_entity.id})
            await self.daoservice.post(address=address_entity, document=new_entity)
            local_tile.data.ids.add(new_entity.id)

        elif local_tile.data.tile_type == TileType.FOREST:
            new_entity: Entity = Entity(id=str(uuid.uuid4()), entity_type=EntityType.TREE)
            address_entity: Address = Address.model_validate({**address.model_dump(), "entity_id": new_entity.id})
            await self.daoservice.post(address=address_entity, document=new_entity)
            local_tile.data.ids.add(new_entity.id)

            new_entity = Entity(id=str(uuid.uuid4()), entity_type=EntityType.MYCELIUM)
            address_entity: Address = Address.model_validate({**address.model_dump(), "entity_id": new_entity.id})
            await self.daoservice.post(address=address_entity, document=new_entity)
            local_tile.data.ids.add(new_entity.id)

        elif local_tile.data.tile_type == TileType.OCEAN:
            new_entity: Entity = Entity(id=str(uuid.uuid4()), entity_type=EntityType.FISH)
            address_entity: Address = Address.model_validate({**address.model_dump(), "entity_id": new_entity.id})
            await self.daoservice.post(address=address_entity, document=new_entity)
            local_tile.data.ids.add(new_entity.id)

        await self.daoservice.patch(address=address, document={"ids": local_tile.data.ids})

    ### entity agent logic
    async def entity_mycelium(self, wrapped_entity: WrappedData[Entity]):
        pass

    async def entity_grass(self, wrapped_entity: WrappedData[Entity]):
        pass

    async def entity_fish(self, wrapped_entity: WrappedData[Entity]):
        pass

    async def entity_tree(self, wrapped_entity: WrappedData[Entity]):
        pass

    ###

    async def grow_entities(self, address: Address):
        # get entities ids for the tile
        local_tile: WrappedData[Tile] = await self.daoservice.get(address=address)

        async def entity_producer(queue: Queue):
            for entity_id in local_tile.data.ids:
                await queue.put(entity_id)

        async def step_one():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_entity_id: str = await queue.get()

                    # TODO: Process entity
                    address_entity: Address = Address.model_validate(
                        {**address.model_dump(), "entity_id": local_entity_id}
                    )
                    wrapped_entity: WrappedData[Entity] = await self.daoservice.get(address=address_entity)
                    # print(wrapped_entity.model_dump())

                    if wrapped_entity.data.entity_type == EntityType.MYCELIUM:
                        await self.entity_mycelium(wrapped_entity=wrapped_entity)
                    # elif wrapped_entity.data.entity_type == EntityType.MUSHROOM:
                    #     pass
                    elif wrapped_entity.data.entity_type == EntityType.GRASS:
                        await self.entity_grass(wrapped_entity=wrapped_entity)
                    elif wrapped_entity.data.entity_type == EntityType.FISH:
                        await self.entity_fish(wrapped_entity=wrapped_entity)
                    elif wrapped_entity.data.entity_type == EntityType.TREE:
                        await self.entity_tree(wrapped_entity=wrapped_entity)
                    # elif wrapped_entity.data.entity_type == EntityType.FRUIT:
                    #     pass

                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(entity_producer(queue), consumer(queue))

        await step_one()
