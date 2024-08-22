import logging

from pydantic import BaseModel

from ...client.dao import DaoClient
from ...sdk.contracts.dtos.entities.entity import Entity
from ...sdk.contracts.dtos.sdk.requests.chunk.create import ChunkCreateRequest
from ...sdk.contracts.dtos.sdk.requests.chunk.delete import ChunkDeleteRequest
from ...sdk.contracts.dtos.sdk.requests.chunk.get import ChunkGetRequest
from ...sdk.contracts.dtos.sdk.requests.world.create import WorldCreateRequest
from ...sdk.contracts.dtos.sdk.requests.world.delete import WorldDeleteRequest
from ...sdk.contracts.dtos.sdk.requests.world.get import WorldGetRequest
from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.dtos.tiles.address import Address
from ...sdk.contracts.dtos.tiles.chunk import Chunk
from ...sdk.contracts.dtos.tiles.tile import Tile
from ...sdk.contracts.dtos.tiles.world import World
from ..factories.chunk.flat import FlatChunkFactory
from ..factories.entity.entity import EntityFactory
from ..factories.world.world import WorldFactory

logger = logging.getLogger()


class StateService(BaseModel):
    daoclient: DaoClient

    world_factory: WorldFactory
    entity_factory: EntityFactory
    flatchunk_factory: FlatChunkFactory

    class Config:
        arbitrary_types_allowed = True

    ### World ##################################

    async def world_create(self, request: WorldCreateRequest) -> str:
        logger.debug("[StateService] creating world")
        return await self.world_factory.create(name=request.name)

    async def world_lite_get(self, request: WorldGetRequest) -> World:
        address_world: Address = Address.model_validate({"world_id": request.id})
        wrapped_world: WrappedData[World] = await self.daoclient.document_get(address=address_world, full=False)
        return wrapped_world.data

    async def world_get(self, request: WorldGetRequest) -> World:
        # TODO: needs conversion to daoclient backend

        # Build a complete World from Lite objects
        address_world: Address = Address.model_validate({"world_id": request.id})

        wrapped_world = await self.daoclient.document_get(address=address_world, full=False)
        world: World = wrapped_world.data

        partial_world = world.model_dump(exclude={"ids"})
        world: World = World.model_validate(partial_world)

        chunk_ids: set[str] = world.ids
        for chunk_id in chunk_ids:
            local_chunk: Chunk = await self.chunk_get(request=ChunkGetRequest(world_id=request.id, chunk_id=chunk_id))
            world.contents[chunk_id] = local_chunk
        return world

    async def world_delete(self, request: WorldDeleteRequest) -> bool:
        logger.debug("[StateService] deleting world")
        address_world: Address = Address.model_validate({"world_id": request.id})
        return await self.daoclient.document_delete(address=address_world)

    ### Chunk ##################################

    async def chunk_create(self, request: ChunkCreateRequest) -> str:
        logger.debug("[StateService] creating chunk")
        new_chunk: Chunk = await self.flatchunk_factory.create(
            world_id=request.world_id, name=request.name, dimensions=request.dimensions, biome=request.biome
        )

        # Entity Factory Terrain Creation
        address_chunk: Address = Address.model_validate({"world_id": request.world_id, "chunk_id": new_chunk.id})
        await self.entity_factory.terrain_generate(address=address_chunk, chunk=new_chunk)

        wrapped_chunk = await self.daoclient.document_get(address=address_chunk, full=False)
        new_chunk: Chunk = wrapped_chunk.data

        # Entity Factory Quantum
        await self.entity_factory.quantum(address=address_chunk, chunk=new_chunk)

        return new_chunk.id

    async def chunk_delete(self, request: ChunkDeleteRequest) -> None:
        msg: str = f"[WorldService] deleting chunk {id}"
        logger.debug(msg)
        address_chunk: Address = Address.model_validate({"world_id": request.world_id, "chunk_id": request.chunk_id})
        await self.daoclient.document_delete(address=address_chunk)

    async def chunk_lite_get(self, request: ChunkGetRequest) -> Chunk:
        address_chunk: Address = Address.model_validate({"world_id": request.world_id, "chunk_id": request.chunk_id})
        response: WrappedData[Chunk] = await self.daoclient.document_get(address=address_chunk, full=False)
        return response.data

    async def chunk_get(self, request: ChunkGetRequest) -> Chunk:
        # Builds a complete Chunk from Lite objects
        address_chunk: Address = Address.model_validate({"world_id": request.world_id, "chunk_id": request.chunk_id})
        wrapped_chunk: WrappedData[Chunk] = await self.daoclient.document_get(address=address_chunk, full=False)
        chunk: Chunk = wrapped_chunk.data

        chunk_partial = chunk.model_dump(exclude={"tile_ids"})
        chunk: Chunk = Chunk.model_validate(chunk_partial)

        # re-hydrate the tiles
        tile_ids: set[str] = chunk.ids
        for tile_id in tile_ids:
            address_tile: Address = Address.model_validate(
                {"world_id": request.world_id, "chunk_id": chunk.id, "tile_id": tile_id}
            )
            tile: Tile = await self.tile_get(address=address_tile)

            # re-hydrate the entities
            entity_ids: set[str] = tile.ids
            for entity_id in entity_ids:
                address_entity: Address = Address.model_validate(
                    {
                        "world_id": request.world_id,
                        "chunk_id": chunk.id,
                        "tile_id": tile_id,
                        "entity_id": entity_id,
                    }
                )
                entity: Entity = await self.entity_get(address=address_entity)

                # add finalized entity to tile
                tile.contents[entity_id] = entity

            # Add finalized tile to chunk
            chunk.contents[tile_id] = tile

        return chunk

    ### Tile ##################################

    async def tile_get(self, address: Address) -> Tile:
        wrapped_tile: WrappedData[Tile] = await self.daoclient.document_get(address=address, full=False)
        return wrapped_tile.data

    ### Entity ##################################

    async def entity_get(self, address: Address) -> Entity:
        wrapped_entity: WrappedData[Entity] = await self.daoclient.document_get(address=address, full=False)
        return wrapped_entity.data
