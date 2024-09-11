import asyncio
import logging
import uuid
from asyncio import Queue

from pydantic import BaseModel

from ....sdk.contracts.dtos.entities.entity import Entity
from ....sdk.contracts.dtos.entities.fauna.fish import EntityFish
from ....sdk.contracts.dtos.entities.flora.grass import EntityGrass
from ....sdk.contracts.dtos.entities.flora.tree import EntityTree
from ....sdk.contracts.dtos.entities.funga.fungi import EntityFungi
from ....sdk.contracts.dtos.tiles.address import Address
from ....sdk.contracts.dtos.tiles.tile import Tile
from ....sdk.contracts.types.entity import EntityType
from ....sdk.contracts.types.tile import TileType
from ...clients.dao import DaoClient

logger = logging.getLogger()


class AbstractEntityFactory(BaseModel):
    daoclient: DaoClient

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    async def producer(ids: set[str], queue: Queue):
        for local_id in ids:
            await queue.put(local_id)

    async def generate(self, address: Address) -> None:
        # get entities ids for the tile
        local_tile: Tile = await self.daoclient.get(address=address)

        # if len(local_tile.ids) > 0:
        #     msg: str = f"entity generation can occurring on a tile with pre-existing entities, {address}"
        #     logger.warning(msg)

        # Review types now
        if local_tile.tile_type == TileType.GRASS:
            new_entity: Entity = Entity(id=str(uuid.uuid4()), entity_type=EntityType.GRASS)
            address_entity: Address = Address.model_validate({**address.model_dump(), "entity_id": new_entity.id})
            await self.daoclient.post(address=address_entity, document=new_entity)
            local_tile.ids.add(new_entity.id)

        elif local_tile.tile_type == TileType.FOREST:
            new_entity: Entity = Entity(id=str(uuid.uuid4()), entity_type=EntityType.TREE)
            address_entity: Address = Address.model_validate({**address.model_dump(), "entity_id": new_entity.id})
            await self.daoclient.post(address=address_entity, document=new_entity)
            local_tile.ids.add(new_entity.id)

            new_entity = Entity(id=str(uuid.uuid4()), entity_type=EntityType.FUNGI)
            address_entity: Address = Address.model_validate({**address.model_dump(), "entity_id": new_entity.id})
            await self.daoclient.post(address=address_entity, document=new_entity)
            local_tile.ids.add(new_entity.id)

        elif local_tile.tile_type == TileType.OCEAN:
            new_entity: Entity = Entity(id=str(uuid.uuid4()), entity_type=EntityType.FISH)
            address_entity: Address = Address.model_validate({**address.model_dump(), "entity_id": new_entity.id})
            await self.daoclient.post(address=address_entity, document=new_entity)
            local_tile.ids.add(new_entity.id)

        patch: dict = {"ids": list(local_tile.ids)}
        # print(f"tile id {local_tile}, got: {patch}")
        await self.daoclient.patch(address=address, document=patch)

    ###

    async def grow_entities(self, address: Address):
        # get entities ids for the tile
        local_tile: Tile = await self.daoclient.get(address=address)

        async def entity_producer(queue: Queue):
            for entity_id in local_tile.ids:
                await queue.put(entity_id)

        async def step_one():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_entity_id: str = await queue.get()

                    # TODO: Process entity
                    address_entity: Address = Address.model_validate(
                        {**address.model_dump(), "entity_id": local_entity_id}
                    )
                    entity: Entity = await self.daoclient.get(address=address_entity)
                    # print(wrapped_entity.model_dump())

                    if entity.entity_type == EntityType.FUNGI:
                        fungi: EntityFungi = EntityFungi.model_validate(entity.model_dump())
                        await fungi.quantum()
                    elif entity.entity_type == EntityType.GRASS:
                        grass: EntityGrass = EntityGrass.model_validate(entity.model_dump())
                        await grass.quantum()
                    elif entity.entity_type == EntityType.FISH:
                        fish: EntityFish = EntityFish.model_validate({**entity.model_dump(), "address": address_entity, "daoclient": self.daoclient })
                        await fish.quantum()
                    elif entity.entity_type == EntityType.TREE:
                        tree: EntityTree = EntityTree.model_validate(entity.model_dump())
                        await tree.quantum()

                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(entity_producer(queue), consumer(queue))

        await step_one()
