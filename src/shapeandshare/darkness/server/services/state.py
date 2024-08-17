import logging

from pydantic import BaseModel

from ...sdk.contracts.dtos.sdk.requests.chunk.create import ChunkCreateRequest
from ...sdk.contracts.dtos.sdk.requests.chunk.delete import ChunkDeleteRequest
from ...sdk.contracts.dtos.sdk.requests.chunk.get import ChunkGetRequest
from ...sdk.contracts.dtos.sdk.requests.world.create import WorldCreateRequest
from ...sdk.contracts.dtos.sdk.requests.world.delete import WorldDeleteRequest
from ...sdk.contracts.dtos.sdk.requests.world.get import WorldGetRequest
from ...sdk.contracts.dtos.tiles.chunk import Chunk
from ...sdk.contracts.dtos.tiles.tile import Tile
from ...sdk.contracts.dtos.tiles.world import World
from ..dao.chunk import ChunkDao
from ..dao.tile import TileDao
from ..dao.world import WorldDao
from ..factories.chunk.flat import FlatChunkFactory
from ..factories.entity.entity import EntityFactory
from ..factories.world.world import WorldFactory

logger = logging.getLogger()


class StateService(BaseModel):
    worlddao: WorldDao
    chunkdao: ChunkDao
    tiledao: TileDao
    world_factory: WorldFactory
    entity_factory: EntityFactory
    flatchunk_factory: FlatChunkFactory

    ### World ##################################

    async def world_create(self, request: WorldCreateRequest) -> str:
        logger.debug("[StateService] creating world")
        return await self.world_factory.create(name=request.name)

    async def world_lite_get(self, request: WorldGetRequest) -> World:
        return World.model_validate((await self.worlddao.get(tokens={"world_id": request.id})).data)

    async def world_get(self, request: WorldGetRequest) -> World:
        # Build a complete World from Lite objects
        world: World = World.model_validate((await self.worlddao.get(tokens={"world_id": request.id})).data)
        chunk_ids: set[str] = world.ids
        partial_world = world.model_dump(exclude={"ids"})
        world: World = World.model_validate(partial_world)
        for chunk_id in chunk_ids:
            local_chunk: Chunk = await self.chunk_get(request=ChunkGetRequest(world_id=request.id, chunk_id=chunk_id))
            world.contents[chunk_id] = local_chunk
        return world

    async def world_delete(self, request: WorldDeleteRequest) -> None:
        logger.debug("[StateService] deleting world")
        await self.worlddao.delete(tokens={"world_id": request.id})

    ### Chunk ##################################

    async def chunk_create(self, request: ChunkCreateRequest) -> str:
        logger.debug("[StateService] creating chunk")
        new_chunk: Chunk = await self.flatchunk_factory.create(
            world_id=request.world_id, name=request.name, dimensions=request.dimensions, biome=request.biome
        )

        # Entity Factory Terrain Creation
        await self.entity_factory.terrain_generate(
            tokens={"world_id": request.world_id, "chunk_id": new_chunk.id}, chunk=new_chunk
        )
        new_chunk: Chunk = Chunk.model_validate(
            (await self.chunkdao.get(tokens={"world_id": request.world_id, "chunk_id": new_chunk.id})).data
        )

        # Entity Factory Quantum
        await self.entity_factory.quantum(
            tokens={"world_id": request.world_id, "chunk_id": new_chunk.id}, chunk=new_chunk
        )

        return new_chunk.id

    async def chunk_delete(self, request: ChunkDeleteRequest) -> None:
        msg: str = f"[WorldService] deleting chunk {id}"
        logger.debug(msg)
        await self.chunkdao.delete(tokens={"world_id": request.world_id, "chunk_id": request.chunk_id})

    async def chunk_lite_get(self, request: ChunkGetRequest) -> Chunk:
        return (await self.chunkdao.get(tokens={"world_id": request.world_id, "chunk_id": request.chunk_id})).data

    async def chunk_get(self, request: ChunkGetRequest) -> Chunk:
        # Builds a complete Chunk from Lite objects
        chunk: Chunk = Chunk.model_validate(
            (await self.chunkdao.get(tokens={"world_id": request.world_id, "chunk_id": request.chunk_id})).data
        )
        tile_ids: set[str] = chunk.ids
        chunk_partial = chunk.model_dump(exclude={"tile_ids"})
        chunk: Chunk = Chunk.model_validate(chunk_partial)

        # re-hydrate the tiles
        for tile_id in tile_ids:
            tile: Tile = Tile.model_validate(
                (
                    await self.tiledao.get(
                        tokens={"world_id": request.world_id, "chunk_id": chunk.id, "tile_id": tile_id}
                    )
                ).data
            )
            chunk.contents[tile_id] = tile

        return chunk
