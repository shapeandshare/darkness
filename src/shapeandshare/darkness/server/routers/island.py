import logging

from fastapi import APIRouter, HTTPException

from ...contracts.dtos.island import Island
from ...contracts.dtos.requests.island_create_request import IslandCreateRequest
from ...contracts.dtos.requests.island_get_request import IslandGetRequest
from ...contracts.dtos.responses.island_create_response import IslandCreateResponse
from ...contracts.dtos.responses.response import Response
from ...contracts.errors.service import ServiceError
from ..context import ContextManager

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
async def island_get(island_get_request: IslandGetRequest) -> Response[Island]:
    msg: str = f"[GET][/island/{island_get_request.id}]"
    logger.debug(msg)

    try:
        island: Island | None = ContextManager.world_service.island_get(
            id=island_get_request.id
        )
    except ServiceError as error:
        logger.warning(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error

    response = Response[Island](data=island)
    msg: str = f"[GET][/island/{response.data.id}] {response.dict()}"
    logger.debug(msg)
    return response
