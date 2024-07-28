import logging

from fastapi import APIRouter, HTTPException

from ...contracts.dtos.island import Island
from ...contracts.dtos.requests.island_create_request import IslandCreateRequest
from ...contracts.dtos.responses.island_create_response import IslandCreateResponse
from ...contracts.dtos.responses.response import Response
from ...contracts.errors.service import ServiceError
from ..context import ContextManager

logger = logging.getLogger()

router: APIRouter = APIRouter(
    prefix="/metrics",
    tags=["metrics"],
    responses={404: {"description": "Not found"}},
)


@router.get("/health")
async def health_get() -> Response[dict]:
    response: Response[dict] = Response[dict](data={"healthy": True})
    return response


# async def health_get( -> Response[IslandCreateResponse]:
# logger.debug("[POST][/island/create]")
# island_id: str = ContextManager.world_service.island_create(
#     request=island_create_request
# )
# response = Response[IslandCreateResponse](data=IslandCreateResponse(id=island_id))
# msg: str = f"[GET][/island/create] {response}"
# logger.debug(msg)
# return response
#
