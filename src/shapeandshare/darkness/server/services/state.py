import logging

from pydantic import BaseModel
from pymongo.results import DeleteResult, UpdateResult

from ...sdk.contracts.dtos.entities.entity import Entity
from ...sdk.contracts.dtos.sdk.requests.chunk.chunk import ChunkRequest
from ...sdk.contracts.dtos.sdk.requests.chunk.create import ChunkCreateRequest
from ...sdk.contracts.dtos.sdk.requests.chunk.delete import ChunkDeleteRequest
from ...sdk.contracts.dtos.sdk.requests.chunk.get import ChunkGetRequest
from ...sdk.contracts.dtos.sdk.requests.chunk.patch import ChunkPatchRequest
from ...sdk.contracts.dtos.sdk.requests.entity.delete import EntityDeleteRequest
from ...sdk.contracts.dtos.sdk.requests.entity.entity import EntityRequest
from ...sdk.contracts.dtos.sdk.requests.entity.patch import EntityPatchRequest
from ...sdk.contracts.dtos.sdk.requests.tile.delete import TileDeleteRequest
from ...sdk.contracts.dtos.sdk.requests.tile.get import TileGetRequest
from ...sdk.contracts.dtos.sdk.requests.tile.patch import TilePatchRequest
from ...sdk.contracts.dtos.sdk.requests.world.create import WorldCreateRequest
from ...sdk.contracts.dtos.sdk.requests.world.delete import WorldDeleteRequest
from ...sdk.contracts.dtos.sdk.requests.world.get import WorldGetRequest
from ...sdk.contracts.dtos.sdk.requests.world.patch import WorldPatchRequest
from ...sdk.contracts.dtos.tiles.address import Address
from ...sdk.contracts.dtos.tiles.chunk import Chunk
from ...sdk.contracts.dtos.tiles.tile import Tile
from ...sdk.contracts.dtos.tiles.world import World
from ...sdk.contracts.types.connection import TileConnectionType
from ...sdk.contracts.types.dao_document import DaoDocumentType
from ..clients.dao import DaoClient
from ..factories.chunk.flat import FlatChunkFactory
from ..factories.entity.entity import EntityFactory
from ..factories.world.world import WorldFactory

logger = logging.getLogger()


# pylint: disable=too-many-public-methods
class StateService(BaseModel):
    daoclient: DaoClient

    world_factory: WorldFactory
    entity_factory: EntityFactory
    flatchunk_factory: FlatChunkFactory

    class Config:
        arbitrary_types_allowed = True

    ### Worlds ##################################

    async def worlds_get(self) -> list[World]:
        return await self.daoclient.get_all(doc_type=DaoDocumentType.WORLD)

    ### World ##################################

    async def world_create(self, request: WorldCreateRequest) -> str:
        logger.debug("[StateService] creating world")
        return await self.world_factory.create(name=request.name)

    async def world_lite_get(self, request: WorldGetRequest) -> World:
        return await self.daoclient.get(address=Address(world_id=request.id))

    async def world_get(self, request: WorldGetRequest) -> World:
        # TODO: needs conversion to daoclient backend

        # Build a complete World from Lite objects
        world: World = await self.daoclient.get(address=Address(world_id=request.id))

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

        if request.cascade:
            world: World = await self.world_get(request=WorldGetRequest(world_id=address_world))
            for chunk_id in world.ids:
                await self.chunk_delete(
                    request=ChunkDeleteRequest(world_id=address_world, chunk_id=chunk_id, cascade=request.cascade)
                )

        # lastly delete the world
        result: DeleteResult = await self.daoclient.delete(address=address_world)
        if result.deleted_count == 1:
            return True
        return False

    async def world_patch(self, request: WorldPatchRequest) -> UpdateResult:
        address_world: Address = Address.model_validate({"world_id": request.world_id})
        return await self.daoclient.patch(address=address_world, document=request.partial)

    ### Chunk ##################################

    async def chunk_create(self, request: ChunkCreateRequest) -> str:
        logger.debug("[StateService] creating chunk")
        new_chunk: Chunk = await self.flatchunk_factory.create(
            world_id=request.world_id, name=request.name, dimensions=request.dimensions, biome=request.biome
        )

        # Entity Factory Terrain Creation
        address_chunk: Address = Address.model_validate({"world_id": request.world_id, "chunk_id": new_chunk.id})
        await self.entity_factory.terrain_generate(address=address_chunk, chunk=new_chunk)

        new_chunk: Chunk = await self.daoclient.get(address=address_chunk)

        # # Entity Factory Quantum
        # await self.entity_factory.quantum(address=address_chunk)

        return new_chunk.id

    async def chunk_patch(self, request: ChunkPatchRequest) -> UpdateResult:
        address_chunk: Address = Address.model_validate({"world_id": request.world_id, "chunk_id": request.chunk_id})
        return await self.daoclient.patch(address=address_chunk, document=request.partial)

    async def chunk_delete(self, request: ChunkDeleteRequest) -> bool:
        msg: str = f"[WorldService] deleting chunk {id}"
        logger.debug(msg)
        address_chunk: Address = Address.model_validate({"world_id": request.world_id, "chunk_id": request.chunk_id})

        if request.parent:
            parent: World = await self.world_get(request=WorldGetRequest(world_id=request.world_id))
            new_ids = [id for id in parent.ids if id != request.chunk_id]
            await self.world_patch(request=WorldPatchRequest(world_id=request.world_id, partial={"ids": new_ids}))

        if request.cascade:
            chunk: Chunk = await self.chunk_get(
                request=ChunkGetRequest(world_id=request.world_id, chunk_id=request.chunk_id)
            )
            for tile_id in chunk.ids:
                await self.tile_delete(
                    request=TileDeleteRequest(
                        world_id=request.world_id,
                        chunk_id=request.chunk_id,
                        tile_id=tile_id,
                        cascade=request.cascade,
                        parent=False,
                    )
                )

        # lastly delete the chunk
        await self.daoclient.delete(address=address_chunk)

        return True

    async def chunk_lite_get(self, request: ChunkGetRequest) -> Chunk:
        address_chunk: Address = Address.model_validate({"world_id": request.world_id, "chunk_id": request.chunk_id})
        return await self.daoclient.get(address=address_chunk)

    async def chunk_get(self, request: ChunkGetRequest) -> Chunk:
        # Builds a complete Chunk from Lite objects
        address_chunk: Address = Address.model_validate({"world_id": request.world_id, "chunk_id": request.chunk_id})
        chunk: Chunk = await self.daoclient.get(address=address_chunk)

        chunk_partial = chunk.model_dump(exclude={"tile_ids"})
        chunk: Chunk = Chunk.model_validate(chunk_partial)

        # re-hydrate the tiles
        tile_ids: set[str] = chunk.ids
        for tile_id in tile_ids:
            tile: Tile = await self.tile_get(
                request=TileGetRequest(world_id=request.world_id, chunk_id=chunk.id, tile_id=tile_id)
            )

            # Add finalized tile to chunk
            chunk.contents[tile_id] = tile

        return chunk

    async def chunk_quantum(self, request: ChunkRequest):
        address: Address = Address(world_id=request.world_id, chunk_id=request.chunk_id)
        await self.flatchunk_factory.quantum(address=address)
        await self.entity_factory.quantum(address=address)

    async def chunk_quantum_tile(self, request: ChunkRequest):
        address: Address = Address(world_id=request.world_id, chunk_id=request.chunk_id)
        await self.flatchunk_factory.quantum(address=address)

    async def chunk_quantum_entity(self, request: ChunkRequest):
        address: Address = Address(world_id=request.world_id, chunk_id=request.chunk_id)
        await self.entity_factory.quantum(address=address)

    ### Tile ##################################

    async def tile_lite_get(self, request: TileGetRequest) -> Tile:
        address_tile: Address = Address.model_validate(
            {"world_id": request.world_id, "chunk_id": request.chunk_id, "tile_id": request.tile_id}
        )
        return await self.daoclient.get(address=address_tile)

    async def tile_get(self, request: TileGetRequest) -> Tile:
        tile: Tile = await self.tile_lite_get(request=request)

        # re-hydrate the entities
        entity_ids: set[str] = tile.ids
        for entity_id in entity_ids:
            entity_request: EntityRequest = EntityRequest.model_validate(
                {
                    "world_id": request.world_id,
                    "chunk_id": request.chunk_id,
                    "tile_id": request.tile_id,
                    "entity_id": entity_id,
                }
            )

            entity: Entity = await self.entity_get(request=entity_request)

            # add finalized entity to tile
            tile.contents[entity_id] = entity

        return tile

    async def tile_patch(self, request: TilePatchRequest) -> UpdateResult:
        address_tile: Address = Address.model_validate(
            {"world_id": request.world_id, "chunk_id": request.chunk_id, "tile_id": request.tile_id}
        )
        return await self.daoclient.patch(address=address_tile, document=request.partial)

    async def tile_delete(self, request: TileDeleteRequest) -> bool:
        address_tile: Address = Address.model_validate(
            {"world_id": request.world_id, "chunk_id": request.chunk_id, "tile_id": request.tile_id}
        )

        # update parent if flagged
        if request.parent:
            parent: Chunk = await self.chunk_get(
                request=ChunkGetRequest(world_id=request.world_id, chunk_id=request.chunk_id)
            )
            new_ids = [id for id in parent.ids if id != request.tile_id]
            await self.chunk_patch(
                request=ChunkPatchRequest(
                    world_id=request.world_id, chunk_id=request.chunk_id, partial={"ids": new_ids}
                )
            )

        # cascade down if flagged
        if request.cascade:
            # 1. Remove all entities
            # 2. Unhook the neighbors

            tile: Tile = await self.tile_get(
                request=TileGetRequest(world_id=request.world_id, chunk_id=request.chunk_id, tile_id=request.tile_id)
            )

            # 1. Remove all entities
            for entity_id in tile.ids:
                await self.entity_delete(
                    request=EntityDeleteRequest(
                        world_id=request.world_id,
                        chunk_id=request.chunk_id,
                        tile_id=request.tile_id,
                        entity_id=entity_id,
                        parent=False,  # Since are are removing the tile in this logic we don't need to update its parent
                    )
                )

            # 2. Unhook the neighbors
            for conn_type, neighbor_id in tile.next.items():
                neighbor: Tile = await self.tile_get(
                    request=TileGetRequest(world_id=request.world_id, chunk_id=request.chunk_id, tile_id=neighbor_id)
                )
                neigh_nexts: dict[TileConnectionType, str] = neighbor.nexts
                targ_conn_type: TileConnectionType = TileConnectionType.opposite(of=conn_type)
                if targ_conn_type not in neigh_nexts:
                    msg: str = f"conn type missing in neighbor, {conn_type} -> {targ_conn_type}"
                    logger.warning(msg)
                else:
                    del neigh_nexts[targ_conn_type]

                    # Update the neighbor
                    await self.tile_patch(
                        request=TilePatchRequest(
                            world_id=request.world_id,
                            chunk_id=request.chunk_id,
                            tile_id=neighbor_id,
                            partial={"next": neigh_nexts},
                        )
                    )

        # 3. lastly delete the tile
        await self.daoclient.delete(address=address_tile)

        return True

    ### Entity ##################################

    async def entity_get(self, request: EntityRequest) -> Entity:
        address_entity: Address = Address.model_validate(
            {
                "world_id": request.world_id,
                "chunk_id": request.chunk_id,
                "tile_id": request.tile_id,
                "entity_id": request.entity_id,
            }
        )
        return await self.daoclient.get(address=address_entity)

    async def entity_patch(self, request: EntityPatchRequest) -> UpdateResult:
        address_entity: Address = Address.model_validate(
            {
                "world_id": request.world_id,
                "chunk_id": request.chunk_id,
                "tile_id": request.tile_id,
                "entity_id": request.entity_id,
            }
        )
        return await self.daoclient.patch(address=address_entity, document=request.partial)

    async def entity_delete(self, request: EntityDeleteRequest) -> bool:
        address_entity: Address = Address.model_validate(
            {
                "world_id": request.world_id,
                "chunk_id": request.chunk_id,
                "tile_id": request.tile_id,
                "entity_id": request.entity_id,
            }
        )

        if request.parent:
            # remove self from containing tile
            tile: Tile = await self.tile_get(
                request=TileGetRequest(world_id=request.world_id, chunk_id=request.chunk_id, tile_id=request.tile_id)
            )
            new_ids: list[str] = [id for id in tile.ids if id != request.entity_id]
            await self.tile_patch(
                request=TilePatchRequest(
                    world_id=request.world_id,
                    chunk_id=request.chunk_id,
                    tile_id=request.tile_id,
                    partial={"ids": new_ids},
                )
            )

        # Lastly delete the entity
        await self.daoclient.delete(address=address_entity)

        return True
