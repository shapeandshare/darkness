import logging

from fastapi import APIRouter, HTTPException

from src.darkness.contracts.dtos.island_create_request import IslandCreateRequest

from ...contracts.dtos.island import Island
from ...contracts.dtos.island_create_response import IslandCreateResponse
from ...contracts.dtos.response import Response
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
    logger.debug(f"[GET][/island/create] {response}")
    return response


@router.get("/{island_id}")
async def island_get(island_id: str) -> Response[str]:
    logger.debug(f"[GET][/island/{island_id}]")
    island: Island | None = ContextManager.world_service.island_get(id=island_id)
    if island:
        response = Response[str](data=island.model_dump())
        logger.debug(f"[GET][/island/{island_id}] {response}")
        return response
    logger.warn(f"[GET][/island/{island_id}] - 404")
    raise HTTPException(status_code=404, detail="Item not found")
