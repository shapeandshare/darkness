import logging

from fastapi import APIRouter, HTTPException

from ....sdk.contracts.dtos.island import Island
from ....sdk.contracts.dtos.sdk.requests.island.create import IslandCreateRequest
from ....sdk.contracts.dtos.sdk.responses.island.create import IslandCreateResponse
from ....sdk.contracts.dtos.sdk.responses.island.get import IslandGetResponse
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ....sdk.contracts.errors.server.service import ServiceError
from ..context import ContextManager

logger = logging.getLogger()

router: APIRouter = APIRouter(
    prefix="/island",
    tags=["island"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def island_create(island_create_request: IslandCreateRequest) -> Response[IslandCreateResponse]:
    logger.debug("[POST][/island]")
    island_id: str = ContextManager.world_service.island_create(request=island_create_request)
    response = Response[IslandCreateResponse](data=IslandCreateResponse(id=island_id))
    msg: str = f"[GET][/island/create] {response}"
    logger.debug(msg)
    return response


@router.get("/{island_id}")
async def island_get(island_id: str) -> Response[IslandGetResponse]:
    msg: str = f"[GET][/island/{island_id}]"
    logger.debug(msg)

    try:
        island: Island = ContextManager.world_service.island_get(id=island_id)
    except ServiceError as error:
        logger.warning(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error

    response = Response[IslandGetResponse](data=IslandGetResponse(island=island))
    msg: str = f"[GET][/island/{response.data.island.id}] {response.model_dump()}"
    logger.debug(msg)
    return response


@router.delete("/{island_id}")
async def island_delete(island_id: str) -> None:
    msg: str = f"[DELETE][/island/{island_id}]"
    logger.debug(msg)

    try:
        ContextManager.world_service.island_delete(id=island_id)
    except ServiceError as error:
        logger.warning(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error

    msg: str = f"[DELETE][/island/{island_id}]"
    logger.debug(msg)
