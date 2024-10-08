import logging

from fastapi import APIRouter

from .....sdk.contracts.dtos.sdk.responses.response import Response
from ..middleware.error import error_handler

logger = logging.getLogger()

router: APIRouter = APIRouter(
    prefix="/metrics",
    tags=["metrics"],
    responses={404: {"description": "Not found"}},
)


@router.get("/health")
@error_handler
async def health_get() -> Response[dict]:
    response: Response[dict] = Response[dict](data={"healthy": True})
    return response
