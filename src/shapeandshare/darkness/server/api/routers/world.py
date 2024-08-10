import logging

from fastapi import APIRouter, HTTPException

from ....sdk.contracts.dtos.island import Island
from ....sdk.contracts.dtos.island_lite import IslandLite
from ....sdk.contracts.dtos.sdk.requests.island.create import IslandCreateRequest
from ....sdk.contracts.dtos.sdk.requests.island.delete import IslandDeleteRequest
from ....sdk.contracts.dtos.sdk.requests.island.get import IslandGetRequest
from ....sdk.contracts.dtos.sdk.requests.world.create import WorldCreateRequest
from ....sdk.contracts.dtos.sdk.requests.world.delete import WorldDeleteRequest
from ....sdk.contracts.dtos.sdk.requests.world.get import WorldGetRequest
from ....sdk.contracts.dtos.sdk.responses.island.create import IslandCreateResponse
from ....sdk.contracts.dtos.sdk.responses.island.get import IslandGetResponse
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ....sdk.contracts.dtos.sdk.responses.world.create import WorldCreateResponse
from ....sdk.contracts.dtos.sdk.responses.world.get import WorldGetResponse
from ....sdk.contracts.dtos.world import World
from ....sdk.contracts.dtos.world_lite import WorldLite
from ....sdk.contracts.errors.server.dao.conflict import DaoConflictError
from ....sdk.contracts.errors.server.dao.doesnotexist import DaoDoesNotExistError
from ....sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError
from ..context import ContextManager

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
            world_lite: WorldLite = await ContextManager.state_service.world_lite_get(request=request)
            response = Response[WorldGetResponse](data=WorldGetResponse(world=world_lite))
    except DaoConflictError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoInconsistencyError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error

    return response


@router.delete("/{world_id}")
async def world_delete(world_id: str) -> None:
    request: WorldDeleteRequest = WorldDeleteRequest(id=world_id)

    try:
        await ContextManager.state_service.world_delete(request=request)
    except DaoConflictError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoInconsistencyError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error


@router.post("")
async def world_create(request: WorldCreateRequest) -> Response[WorldCreateResponse]:
    try:
        world_id: str = await ContextManager.state_service.world_create(request=request)
    except DaoConflictError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoInconsistencyError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error

    response = Response[WorldCreateResponse](data=WorldCreateResponse(id=world_id))
    return response


### /world/world_id/island/


@router.post("/{world_id}/island")
async def island_create(world_id: str, island_create_request: IslandCreateRequest) -> Response[IslandCreateResponse]:
    # we ignore any passed in world_ids in this condition and over-write based on path.
    # Due to this world_id is optional within the DTO.
    island_create_request.world_id = world_id

    try:
        island_id: str = await ContextManager.state_service.island_create(request=island_create_request)
    except DaoConflictError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoInconsistencyError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error

    return Response[IslandCreateResponse](data=IslandCreateResponse(id=island_id))


@router.get("/{world_id}/island/{island_id}")
async def island_get(world_id: str, island_id: str, full: bool = True) -> Response[IslandGetResponse]:
    request: IslandGetRequest = IslandGetRequest(world_id=world_id, island_id=island_id)

    try:
        if full:
            island: Island = await ContextManager.state_service.island_get(request=request)
            response = Response[IslandGetResponse](data=IslandGetResponse(island=island))
        else:
            island_lite: IslandLite = await ContextManager.state_service.island_lite_get(request=request)
            response = Response[IslandGetResponse](data=IslandGetResponse(island=island_lite))
    except DaoConflictError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoInconsistencyError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error

    return response


@router.delete("/{world_id}/island/{island_id}")
async def island_delete(world_id: str, island_id: str) -> None:
    request: IslandDeleteRequest = IslandDeleteRequest(world_id=world_id, island_id=island_id)
    try:
        await ContextManager.state_service.island_delete(request=request)
    except DaoConflictError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoInconsistencyError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
