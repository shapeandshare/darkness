import logging

from fastapi import APIRouter

from ...contracts.dtos.responses.islands_get_response import IslandsGetResponse
from ...contracts.dtos.responses.response import Response
from ..context import ContextManager

logger = logging.getLogger()

router: APIRouter = APIRouter(
    prefix="/islands",
    tags=["islands"],
)


@router.post("/")
async def islands_get() -> Response[IslandsGetResponse]:
    logger.debug("[GET][/islands]")
    islands: list[str] = ContextManager.world_service.islands_get()
    response = Response[IslandsGetResponse](data=IslandsGetResponse(ids=islands))
    msg: str = f"[GET][/islands] {response}"
    logger.debug(msg)
    return response
