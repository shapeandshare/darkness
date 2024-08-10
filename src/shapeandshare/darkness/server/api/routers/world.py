import logging

from fastapi import APIRouter

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
    # logger.debug(f"[GET][/world], full? {full}")

    if full:
        world: World = ContextManager.state_service.world_get(request=request)
        response = Response[WorldGetResponse](data=WorldGetResponse(world=world))
    else:
        world_lite: WorldLite = ContextManager.state_service.world_lite_get(request=request)
        response = Response[WorldGetResponse](data=WorldGetResponse(world=world_lite))

    # msg: str = f"[GET][/islands] {response}"
    # logger.debug(msg)
    return response


@router.delete("/{world_id}")
async def world_delete(world_id: str) -> None:
    request: WorldDeleteRequest = WorldDeleteRequest(id=world_id)
    logger.debug(f"[DELETE][/{world_id}]")
    ContextManager.state_service.world_delete(request=request)


@router.post("/")
async def world_create(request: WorldCreateRequest) -> Response[WorldCreateResponse]:
    world_id: str = ContextManager.state_service.world_create(request=request)
    response = Response[WorldCreateResponse](data=WorldCreateResponse(world_id=world_id))
    return response


### /world/world_id/island/


@router.post("/{world_id}/island")
async def island_create(world_id: str, island_create_request: IslandCreateRequest) -> Response[IslandCreateResponse]:
    logger.debug("[POST][/island]")
    # we ignore any passed in world_ids in this condition and over-write based on path.
    # Due to this world_id is optional within the DTO.
    island_create_request.world_id = world_id
    island_id: str = ContextManager.state_service.island_create(request=island_create_request)
    response = Response[IslandCreateResponse](data=IslandCreateResponse(id=island_id))
    msg: str = f"[GET][/island/create] {response}"
    logger.debug(msg)
    return response


@router.get("/{world_id}/island/{island_id}")
async def island_get(world_id: str, island_id: str, full: bool = True) -> Response[IslandGetResponse]:
    request: IslandGetRequest = IslandGetRequest(world_id=world_id, island_id=island_id)
    # msg: str = f"[GET][/island/{island_get_request.island_id}] full? {full}"
    # logger.debug(msg)

    if full:
        island: Island = ContextManager.state_service.island_get(request=request)
        response = Response[IslandGetResponse](data=IslandGetResponse(island=island))
    else:
        island_lite: IslandLite = ContextManager.state_service.island_lite_get(request=request)
        response = Response[IslandGetResponse](data=IslandGetResponse(island=island_lite))
    # try:
    #     island: Island = ContextManager.state_service.island_get(id=island_id)
    # except ServiceError as error:
    #     logger.warning(str(error))
    #     raise HTTPException(status_code=404, detail=str(error)) from error

    msg: str = f"[GET][/island/{response.data.island.id}] {response.model_dump()}"
    logger.debug(msg)
    return response


@router.delete("/{world_id}/island/{island_id}")
async def island_delete(world_id: str, island_id: str) -> None:
    # msg: str = f"[DELETE][/island/{island_delete_request.island_id}]"
    # logger.debug(msg)
    request: IslandDeleteRequest = IslandDeleteRequest(world_id=world_id, island_id=island_id)
    ContextManager.state_service.island_delete(request=request)
    # try:
    #     ContextManager.state_service.island_delete(request=island_delete_request)
    # except ServiceError as error:
    #     logger.warning(str(error))
    #     raise HTTPException(status_code=404, detail=str(error)) from error

    msg: str = f"[DELETE][/island/{request.island_id}]"
    logger.debug(msg)
