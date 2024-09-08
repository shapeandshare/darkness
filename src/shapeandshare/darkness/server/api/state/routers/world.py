from fastapi import APIRouter, HTTPException

from .....sdk.contracts.dtos.sdk.requests.chunk.chunk import ChunkRequest
from .....sdk.contracts.dtos.sdk.requests.chunk.create import ChunkCreateRequest
from .....sdk.contracts.dtos.sdk.requests.chunk.get import ChunkGetRequest
from .....sdk.contracts.dtos.sdk.requests.chunk.quantum import ChunkQuantumRequest
from .....sdk.contracts.dtos.sdk.requests.world.create import WorldCreateRequest
from .....sdk.contracts.dtos.sdk.requests.world.get import WorldGetRequest
from .....sdk.contracts.dtos.sdk.requests.world.world import WorldRequest
from .....sdk.contracts.dtos.sdk.responses.chunk.create import ChunkCreateResponse
from .....sdk.contracts.dtos.sdk.responses.chunk.get import ChunkGetResponse
from .....sdk.contracts.dtos.sdk.responses.response import Response
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
async def world_delete(world_id: str) -> None:
    request: WorldRequest = WorldRequest(id=world_id)
    await ContextManager.state_service.world_delete(request=request)


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
async def chunk_delete(world_id: str, chunk_id: str) -> None:
    request: ChunkRequest = ChunkRequest(world_id=world_id, chunk_id=chunk_id)
    await ContextManager.state_service.chunk_delete(request=request)


@router.post("/{world_id}/chunk/{chunk_id}")
@error_handler
async def chunk_quantum(world_id: str, chunk_id: str, request: ChunkQuantumRequest) -> None:
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
