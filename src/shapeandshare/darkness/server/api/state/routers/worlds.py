import logging
import traceback

from fastapi import APIRouter, HTTPException

from .....sdk.contracts.dtos.sdk.responses.response import Response
from .....sdk.contracts.dtos.sdk.responses.worlds.get import WorldsGetResponse
from .....sdk.contracts.dtos.tiles.world import World
from .....sdk.contracts.errors.server.dao.conflict import DaoConflictError
from .....sdk.contracts.errors.server.dao.doesnotexist import DaoDoesNotExistError
from .....sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError
from .....sdk.contracts.errors.server.dao.unknown import DaoUnknownError
from ..context import ContextManager

logger = logging.getLogger()

router: APIRouter = APIRouter(
    prefix="/worlds",
    tags=["worlds"],
)


### /worlds


@router.get("")
async def worlds_get() -> Response[WorldsGetResponse]:
    try:
        worlds: list[World] = await ContextManager.state_service.worlds_get()
        response: WorldsGetResponse = WorldsGetResponse(worlds=worlds)
        return Response[WorldsGetResponse](data=response)
    except HTTPException as error:
        logger.error(str(error))
        raise error from error
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoUnknownError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
