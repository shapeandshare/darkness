from fastapi import APIRouter

from .....sdk.contracts.dtos.sdk.responses.response import Response
from .....sdk.contracts.dtos.sdk.responses.worlds.get import WorldsGetResponse
from .....sdk.contracts.dtos.tiles.world import World
from ...common.middleware.error import error_handler
from ..context import ContextManager

router: APIRouter = APIRouter(
    prefix="/worlds",
    tags=["worlds"],
)


### /worlds


@router.get("")
@error_handler
async def worlds_get() -> Response[WorldsGetResponse]:
    worlds: list[World] = await ContextManager.state_service.worlds_get()
    response: WorldsGetResponse = WorldsGetResponse(worlds=worlds)
    return Response[WorldsGetResponse](data=response)
