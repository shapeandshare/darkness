import logging

from fastapi import APIRouter

from ....sdk.contracts.dtos.sdk.requests.world.create import WorldCreateRequest
from ....sdk.contracts.dtos.sdk.requests.world.delete import WorldDeleteRequest
from ....sdk.contracts.dtos.sdk.requests.world.get import WorldGetRequest
from ....sdk.contracts.dtos.sdk.responses.islands.get import IslandsGetResponse
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ....sdk.contracts.dtos.sdk.responses.world.get import WorldGetResponse
from ....sdk.contracts.dtos.world import World
from ....sdk.contracts.dtos.world_lite import WorldLite
from ..context import ContextManager

logger = logging.getLogger()

router: APIRouter = APIRouter(
    prefix="/world",
    tags=["world"],
)


@router.get("/{world_id}")
async def world_get(world_id: str, full: bool = False) -> Response[WorldGetResponse]:
    request: WorldGetRequest = WorldGetRequest(id=world_id)
    logger.debug(f"[GET][/world], full? {full}")

    if full:
        world: World = ContextManager.state_service.world_get(request=request)
        response = Response[WorldGetResponse](data=WorldGetResponse(world=world))
    else:
        world_lite: WorldLite = ContextManager.state_service.world_lite_get(request=request)
        response = Response[WorldGetResponse](data=WorldGetResponse(world=world_lite))

    msg: str = f"[GET][/islands] {response}"
    logger.debug(msg)
    return response


@router.delete("/{world_id}")
async def world_delete(world_id: str) -> None:
    request: WorldDeleteRequest = WorldDeleteRequest(id=world_id)
    logger.debug(f"[DELETE][/{world_id}]")
    ContextManager.state_service.world_delete(request=request)


@router.post("/")
async def world_create(request: WorldCreateRequest) -> str:
    return ContextManager.state_service.world_create(request=request)
