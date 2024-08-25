import logging
import traceback
from http.client import HTTPException

from fastapi import APIRouter

from .....sdk.contracts.dtos.tiles.world import World
from .....sdk.contracts.errors.server.dao.conflict import DaoConflictError
from .....sdk.contracts.errors.server.dao.doesnotexist import DaoDoesNotExistError
from .....sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError
from ..context import ContextManager

logger = logging.getLogger()

router: APIRouter = APIRouter(
    prefix="/chrono",
    tags=["chrono"],
)


async def world_chrono():
    worlds: list[World] = await ContextManager.client.worlds_get()
    for world in worlds:
        for chunk_id in world.ids:
            await ContextManager.client.chunk_quantum(world_id=world.id, chunk_id=chunk_id)


@router.post("")
async def chunk_quantum() -> None:
    try:
        await world_chrono()
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
