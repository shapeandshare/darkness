from fastapi import APIRouter, HTTPException

from ..... import Entity, Tile
from .....sdk.contracts.dtos.sdk.requests.chunk.chunk import ChunkRequest
from .....sdk.contracts.dtos.sdk.requests.chunk.create import ChunkCreateRequest
from .....sdk.contracts.dtos.sdk.requests.chunk.delete import ChunkDeleteRequest
from .....sdk.contracts.dtos.sdk.requests.chunk.get import ChunkGetRequest
from .....sdk.contracts.dtos.sdk.requests.chunk.patch import ChunkPatchRequest
from .....sdk.contracts.dtos.sdk.requests.chunk.quantum import ChunkQuantumRequest
from .....sdk.contracts.dtos.sdk.requests.entity.delete import EntityDeleteRequest
from .....sdk.contracts.dtos.sdk.requests.entity.entity import EntityRequest
from .....sdk.contracts.dtos.sdk.requests.entity.patch import EntityPatchRequest
from .....sdk.contracts.dtos.sdk.requests.tile.delete import TileDeleteRequest
from .....sdk.contracts.dtos.sdk.requests.tile.get import TileGetRequest
from .....sdk.contracts.dtos.sdk.requests.tile.patch import TilePatchRequest
from .....sdk.contracts.dtos.sdk.requests.world.create import WorldCreateRequest
from .....sdk.contracts.dtos.sdk.requests.world.delete import WorldDeleteRequest
from .....sdk.contracts.dtos.sdk.requests.world.get import WorldGetRequest
from .....sdk.contracts.dtos.sdk.requests.world.patch import WorldPatchRequest
from .....sdk.contracts.dtos.sdk.responses.chunk.create import ChunkCreateResponse
from .....sdk.contracts.dtos.sdk.responses.chunk.get import ChunkGetResponse
from .....sdk.contracts.dtos.sdk.responses.entity.get import EntityGetResponse
from .....sdk.contracts.dtos.sdk.responses.response import Response
from .....sdk.contracts.dtos.sdk.responses.tile.get import TileGetResponse
from .....sdk.contracts.dtos.sdk.responses.world.create import WorldCreateResponse
from .....sdk.contracts.dtos.sdk.responses.world.get import WorldGetResponse
from .....sdk.contracts.dtos.tiles.chunk import Chunk
from .....sdk.contracts.dtos.tiles.world import World
from .....sdk.contracts.types.chunk_quantum import ChunkQuantumType
from ...common.middleware.error import error_handler
from ..context import ContextManager

# from pyinstrument import Profiler


router: APIRouter = APIRouter(
    prefix="/world",
    tags=["world"],
)


### /world


@router.get("/{world_id}")
@error_handler
async def world_get(world_id: str, full: bool = False) -> Response[WorldGetResponse]:
    request: WorldGetRequest = WorldGetRequest(id=world_id)

    if full:
        world: World = await ContextManager.state_service.world_get(request=request)
        response = Response[WorldGetResponse](data=WorldGetResponse(world=world))
    else:
        world_lite: World = await ContextManager.state_service.world_lite_get(request=request)
        response = Response[WorldGetResponse](data=WorldGetResponse(world=world_lite))

    return response


@router.delete("/{world_id}")
@error_handler
async def world_delete(world_id: str, cascade: bool) -> Response[bool]:
    request: WorldDeleteRequest = WorldDeleteRequest(id=world_id, cascade=cascade)
    success: bool = await ContextManager.state_service.world_delete(request=request)
    return Response[bool](data=success)


@router.patch("/{world_id}")
@error_handler
async def world_patch(world_id: str, partial: dict) -> Response[bool]:
    request: WorldPatchRequest = WorldPatchRequest(id=world_id, partial=partial)
    await ContextManager.state_service.world_patch(request=request)
    return Response[bool](data=True)


@router.post("")
@error_handler
async def world_create(request: WorldCreateRequest) -> Response[WorldCreateResponse]:
    world_id: str = await ContextManager.state_service.world_create(request=request)
    return Response[WorldCreateResponse](data=WorldCreateResponse(id=world_id))


### /world/world_id/chunk/


@router.post("/{world_id}/chunk")
@error_handler
async def chunk_create(world_id: str, request: ChunkCreateRequest) -> Response[ChunkCreateResponse]:
    # we ignore any passed in world_ids in this condition and over-write based on path.
    # Due to this world_id is optional within the DTO.
    request.world_id = world_id

    # with Profiler() as profiler:
    chunk_id: str = await ContextManager.state_service.chunk_create(request=request)
    # profiler.print()
    return Response[ChunkCreateResponse](data=ChunkCreateResponse(id=chunk_id))


@router.patch("/{world_id}/chunk/{chunk_id}")
@error_handler
async def chunk_patch(world_id: str, chunk_id: str, partial: dict) -> Response[bool]:
    request: ChunkPatchRequest = ChunkPatchRequest(id=world_id, chunk_id=chunk_id, partial=partial)
    await ContextManager.state_service.chunk_patch(request=request)
    return Response[bool](data=ChunkCreateResponse(id=True))


@router.get("/{world_id}/chunk/{chunk_id}")
@error_handler
async def chunk_get(world_id: str, chunk_id: str, full: bool = True) -> Response[ChunkGetResponse]:
    request: ChunkGetRequest = ChunkGetRequest(world_id=world_id, chunk_id=chunk_id)

    if full:
        chunk: Chunk = await ContextManager.state_service.chunk_get(request=request)
        response = Response[ChunkGetResponse](data=ChunkGetResponse(chunk=chunk))
    else:
        chunk: Chunk = await ContextManager.state_service.chunk_lite_get(request=request)
        response = Response[ChunkGetResponse](data=ChunkGetResponse(chunk=chunk))

    return response


@router.delete("/{world_id}/chunk/{chunk_id}")
@error_handler
async def chunk_delete(world_id: str, chunk_id: str, parent: bool, cascade: bool) -> Response[bool]:
    request: ChunkDeleteRequest = ChunkDeleteRequest(
        world_id=world_id, chunk_id=chunk_id, parent=parent, cascade=cascade
    )
    success: bool = await ContextManager.state_service.chunk_delete(request=request)
    return Response[bool](data=success)


@router.post("/{world_id}/chunk/{chunk_id}")
@error_handler
async def chunk_quantum(world_id: str, chunk_id: str, request: ChunkQuantumRequest) -> Response[bool]:
    chunk_request: ChunkRequest = ChunkRequest(world_id=world_id, chunk_id=chunk_id)
    if request.scope == ChunkQuantumType.ALL:
        await ContextManager.state_service.chunk_quantum(request=chunk_request)
    elif request.scope == ChunkQuantumType.ENTITY:
        await ContextManager.state_service.chunk_quantum_entity(request=chunk_request)
    elif request.scope == ChunkQuantumType.TILE:
        await ContextManager.state_service.chunk_quantum_tile(request=chunk_request)
    else:
        msg: str = f"unknown scope ({request.scope})"
        raise HTTPException(status_code=400, detail=msg)
    return Response[bool](data=True)


### /world/{world_id}/chunk/{chunk_id}/tile

### /world/{world_id}/chunk/{chunk_id}/tile/{tile_id}


## get
@router.get("/{world_id}/chunk/{chunk_id}/tile/{tile_id}")
@error_handler
async def tile_get(world_id: str, chunk_id: str, tile_id: str, full: bool = True) -> Response[TileGetResponse]:
    request: TileGetRequest = TileGetRequest(world_id=world_id, chunk_id=chunk_id, tile_id=tile_id)

    if full:
        tile: Tile = await ContextManager.state_service.tile_get(request=request)
        response = Response[TileGetResponse](data=TileGetResponse(tile=tile))
    else:
        tile: Tile = await ContextManager.state_service.tile_lite_get(request=request)
        response = Response[TileGetResponse](data=TileGetResponse(tile=tile))

    return response


## patch
@router.patch("/{world_id}/chunk/{chunk_id}/tile/{tile_id}")
@error_handler
async def tile_patch(world_id: str, chunk_id: str, tile_id: str, partial: dict) -> Response[bool]:
    request: TilePatchRequest = TilePatchRequest(world_id=world_id, chunk_id=chunk_id, tile_id=tile_id, partial=partial)
    await ContextManager.state_service.tile_patch(request=request)
    return Response[bool](data=True)


@router.delete("/{world_id}/chunk/{chunk_id}/tile/{tile_id}")
@error_handler
async def tile_delete(world_id: str, chunk_id: str, tile_id: str, parent: bool, cascade: bool) -> Response[bool]:
    request: TileDeleteRequest = TileDeleteRequest(
        world_id=world_id, chunk_id=chunk_id, tile_id=tile_id, parent=parent, cascade=cascade
    )
    success: bool = await ContextManager.state_service.tile_delete(request=request)
    return Response[bool](data=success)


## get
@router.get("/{world_id}/chunk/{chunk_id}/tile/{tile_id}/entity/{entity_id}")
@error_handler
async def entity_get(world_id: str, chunk_id: str, tile_id: str, entity_id: str) -> Response[EntityGetResponse]:
    request: EntityRequest = EntityRequest(world_id=world_id, chunk_id=chunk_id, tile_id=tile_id, entity_id=entity_id)
    entity: Entity = await ContextManager.state_service.entity_get(request=request)
    return Response[EntityGetResponse](data=EntityGetResponse(entity=entity))


## patch
@router.patch("/{world_id}/chunk/{chunk_id}/tile/{tile_id}/entity/{entity_id}")
@error_handler
async def entity_patch(world_id: str, chunk_id: str, tile_id: str, entity_id: str, partial: dict) -> Response[bool]:
    request: EntityPatchRequest = EntityPatchRequest(
        world_id=world_id, chunk_id=chunk_id, tile_id=tile_id, entity_id=entity_id, partial=partial
    )
    await ContextManager.state_service.entity_patch(request=request)
    return Response[bool](data=True)


### /world/{world_id}/chunk/{chunk_id}/tile/{tile_id}/entity/{entity_id}
## delete
@router.delete("/{world_id}/chunk/{chunk_id}/tile/{tile_id}/entity/{entity_id}")
@error_handler
async def entity_delete(world_id: str, chunk_id: str, tile_id: str, entity_id: str, parent: bool) -> Response[bool]:
    request: EntityDeleteRequest = EntityDeleteRequest(
        world_id=world_id, chunk_id=chunk_id, tile_id=tile_id, entity_id=entity_id, parent=parent
    )
    success: bool = await ContextManager.state_service.entity_delete(request=request)
    return Response[bool](data=success)


### /world/{world_id}/chunk/{chunk_id}/tile/{tile_id}/entity
## post (create)
