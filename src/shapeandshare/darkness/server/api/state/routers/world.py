import logging
import traceback

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
from .....sdk.contracts.errors.server.dao.conflict import DaoConflictError
from .....sdk.contracts.errors.server.dao.doesnotexist import DaoDoesNotExistError
from .....sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError
from .....sdk.contracts.errors.server.dao.unknown import DaoUnknownError
from .....sdk.contracts.types.chunk_quantum import ChunkQuantumType
from ..context import ContextManager

# from pyinstrument import Profiler


logger = logging.getLogger()

router: APIRouter = APIRouter(
    prefix="/world",
    tags=["world"],
)


### /world


@router.get("/{world_id}")
async def world_get(world_id: str, full: bool = False) -> Response[WorldGetResponse]:
    request: WorldGetRequest = WorldGetRequest(id=world_id)

    try:
        if full:
            world: World = await ContextManager.state_service.world_get(request=request)
            response = Response[WorldGetResponse](data=WorldGetResponse(world=world))
        else:
            world_lite: World = await ContextManager.state_service.world_lite_get(request=request)
            response = Response[WorldGetResponse](data=WorldGetResponse(world=world_lite))
    except HTTPException as error:
        logger.error(str(error))
        raise error from error
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoUnknownError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error

    return response


@router.delete("/{world_id}")
async def world_delete(world_id: str) -> None:
    request: WorldRequest = WorldRequest(id=world_id)

    try:
        await ContextManager.state_service.world_delete(request=request)
    except HTTPException as error:
        logger.error(str(error))
        raise error from error
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoUnknownError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error


@router.post("")
async def world_create(request: WorldCreateRequest) -> Response[WorldCreateResponse]:
    try:
        world_id: str = await ContextManager.state_service.world_create(request=request)
    except HTTPException as error:
        logger.error(str(error))
        raise error from error
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoUnknownError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error

    return Response[WorldCreateResponse](data=WorldCreateResponse(id=world_id))


### /world/world_id/chunk/


@router.post("/{world_id}/chunk")
async def chunk_create(world_id: str, request: ChunkCreateRequest) -> Response[ChunkCreateResponse]:
    # we ignore any passed in world_ids in this condition and over-write based on path.
    # Due to this world_id is optional within the DTO.
    request.world_id = world_id

    try:
        # with Profiler() as profiler:
        chunk_id: str = await ContextManager.state_service.chunk_create(request=request)
        # profiler.print()
    except HTTPException as error:
        logger.error(str(error))
        raise error from error
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoUnknownError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(error)
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error

    return Response[ChunkCreateResponse](data=ChunkCreateResponse(id=chunk_id))


@router.get("/{world_id}/chunk/{chunk_id}")
async def chunk_get(world_id: str, chunk_id: str, full: bool = True) -> Response[ChunkGetResponse]:
    request: ChunkGetRequest = ChunkGetRequest(world_id=world_id, chunk_id=chunk_id)

    try:
        if full:
            chunk: Chunk = await ContextManager.state_service.chunk_get(request=request)
            response = Response[ChunkGetResponse](data=ChunkGetResponse(chunk=chunk))
        else:
            chunk: Chunk = await ContextManager.state_service.chunk_lite_get(request=request)
            response = Response[ChunkGetResponse](data=ChunkGetResponse(chunk=chunk))
    except HTTPException as error:
        logger.error(str(error))
        raise error from error
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoUnknownError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error

    return response


@router.delete("/{world_id}/chunk/{chunk_id}")
async def chunk_delete(world_id: str, chunk_id: str) -> None:
    request: ChunkRequest = ChunkRequest(world_id=world_id, chunk_id=chunk_id)
    try:
        await ContextManager.state_service.chunk_delete(request=request)
    except HTTPException as error:
        logger.error(str(error))
        raise error from error
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoUnknownError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error


@router.post("/{world_id}/chunk/{chunk_id}")
async def chunk_quantum(world_id: str, chunk_id: str, request: ChunkQuantumRequest) -> None:
    try:
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
    except HTTPException as error:
        logger.error(str(error))
        raise error from error
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoUnknownError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
