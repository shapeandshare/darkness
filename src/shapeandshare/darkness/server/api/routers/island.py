import logging

from fastapi import APIRouter, HTTPException

from ....sdk.contracts.dtos.island import Island
from ....sdk.contracts.dtos.island_lite import IslandLite
from ....sdk.contracts.dtos.sdk.requests.island.create import IslandCreateRequest
from ....sdk.contracts.dtos.sdk.requests.island.delete import IslandDeleteRequest
from ....sdk.contracts.dtos.sdk.requests.island.get import IslandGetRequest
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
    island_id: str = ContextManager.state_service.island_create(request=island_create_request)
    response = Response[IslandCreateResponse](data=IslandCreateResponse(id=island_id))
    msg: str = f"[GET][/island/create] {response}"
    logger.debug(msg)
    return response


@router.get("/{island_id}")
async def island_get(island_get_request: IslandGetRequest, full: bool = True) -> Response[IslandGetResponse]:
    msg: str = f"[GET][/island/{island_get_request.island_id}] full? {full}"
    logger.debug(msg)

    if full:
        island: Island = ContextManager.state_service.island_get(request=island_get_request)
        response = Response[IslandGetResponse](data=IslandGetResponse(island=island))
    else:
        island_lite: IslandLite = ContextManager.state_service.island_lite_get(request=island_get_request)
        response = Response[IslandGetResponse](data=IslandGetResponse(island=island_lite))
    # try:
    #     island: Island = ContextManager.state_service.island_get(id=island_id)
    # except ServiceError as error:
    #     logger.warning(str(error))
    #     raise HTTPException(status_code=404, detail=str(error)) from error

    msg: str = f"[GET][/island/{response.data.island.id}] {response.model_dump()}"
    logger.debug(msg)
    return response


@router.delete("/{island_id}")
async def island_delete(island_delete_request: IslandDeleteRequest) -> None:
    msg: str = f"[DELETE][/island/{island_delete_request.island_id}]"
    logger.debug(msg)

    ContextManager.state_service.island_delete(request=island_delete_request)
    # try:
    #     ContextManager.state_service.island_delete(request=island_delete_request)
    # except ServiceError as error:
    #     logger.warning(str(error))
    #     raise HTTPException(status_code=404, detail=str(error)) from error

    msg: str = f"[DELETE][/island/{island_delete_request.island_id}]"
    logger.debug(msg)
