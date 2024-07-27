from fastapi import APIRouter, HTTPException
from ..context import ContextManager
from ...contracts.dtos.island import Island

import logging
logger = logging.getLogger()

# from ...contracts.dtos.island import Island
#
router: APIRouter = APIRouter(
    prefix="/island",
    tags=["island"],
    responses={404: {"description": "Not found"}},
)

@router.get("/create")
async def island_create():
    logger.debug("[GET][/island/create]")
    island_id: str = ContextManager.world_service.island_create()
    response: dict = { "data": { "id": island_id }}
    logger.debug(f"[GET][/island/create] {response}")
    return response

    # print(f"[get_island] island_service is {type(context.island_service)}")
    # island: Island | None = context.island_service.get(id=island_id)
    # if island:
    #     return {"data": island.model_dump()}
    # raise HTTPException(status_code=404, detail="Item not found")


@router.get("/{island_id}")
async def island_get(island_id: str):
    logger.debug(f"[GET][/island/{island_id}]")
    # print(f"[get_island] island_service is {type(context.island_service)}")
    island: Island | None = ContextManager.world_service.island_get(id=island_id)
    if island:
        response: dict = {"data": island.model_dump()}
        logger.debug(f"[GET][/island/{island_id}] {response}")
        return response
    logger.warn(f"[GET][/island/{island_id}] - 404")
    raise HTTPException(status_code=404, detail="Item not found")
