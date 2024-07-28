import logging

from fastapi import APIRouter, HTTPException

from ...contracts.dtos.island import Island
from ...contracts.dtos.requests.island_create_request import \
    IslandCreateRequest
from ...contracts.dtos.responses.island_create_response import \
    IslandCreateResponse
from ...contracts.dtos.responses.response import Response
from ..context import ContextManager
from ...contracts.errors.service import ServiceError

logger = logging.getLogger()

router: APIRouter = APIRouter(
    prefix="/island",
    tags=["island"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create")
async def island_create(
    island_create_request: IslandCreateRequest,
) -> Response[IslandCreateResponse]:
    logger.debug("[POST][/island/create]")
    island_id: str = ContextManager.world_service.island_create(
        request=island_create_request
    )
    response = Response[IslandCreateResponse](data=IslandCreateResponse(id=island_id))
    msg: str = f"[GET][/island/create] {response}"
    logger.debug(msg)
    return response


@router.get("/{island_id}")
async def island_get(island_id: str) -> Response[str]:
    msg: str = f"[GET][/island/{island_id}]"
    logger.debug(msg)

    try:
        island: Island | None = ContextManager.world_service.island_get(id=island_id)
    except ServiceError as error:
        logger.warn(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error

    response = Response[str](data=island.model_dump())
    msg: str = f"[GET][/island/{island_id}] {response}"
    logger.debug(msg)
    return response
