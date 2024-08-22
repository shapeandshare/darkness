import logging
import traceback

from fastapi import APIRouter, HTTPException

from .....sdk.contracts.dtos.entities.entity import Entity
from .....sdk.contracts.dtos.sdk.requests.document.document import DocumentRequest
from .....sdk.contracts.dtos.sdk.responses.response import Response
from .....sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from .....sdk.contracts.dtos.tiles.address import Address
from .....sdk.contracts.dtos.tiles.chunk import Chunk
from .....sdk.contracts.dtos.tiles.tile import Tile
from .....sdk.contracts.dtos.tiles.world import World
from .....sdk.contracts.errors.server.dao.conflict import DaoConflictError
from .....sdk.contracts.errors.server.dao.doesnotexist import DaoDoesNotExistError
from .....sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError
from ..context import ContextManager

# from pyinstrument import Profiler


logger = logging.getLogger()

router: APIRouter = APIRouter(
    prefix="/dao",
    tags=["dao"],
)


########################################################
### /dao/world/{world_id}
########################################################


@router.get("/world/{world_id}")
async def world_get(world_id: str, full: bool = False) -> Response[WrappedData[World]]:
    try:
        request: DocumentRequest = DocumentRequest(address=Address(world_id=world_id), full=full)
        wrapped_document: dict = await ContextManager.daoservice.get(request=request)
        response = Response[WrappedData[World]](data=wrapped_document)
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
    return response


@router.delete("/world/{world_id}")
async def world_delete(world_id: str) -> Response[bool]:
    try:
        request: DocumentRequest = DocumentRequest(address=Address(world_id=world_id))
        success: bool = await ContextManager.daoservice.delete(request=request)
        response = Response[bool](data=success)
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
    return response


@router.patch("/world/{world_id}")
async def world_patch(world_id: str, document: dict) -> Response[WrappedData[World]]:
    try:
        if "id" in document:
            assert world_id == document["id"]
        address: Address = Address(world_id=world_id)
        result: dict = await ContextManager.daoservice.patch(address=address, document=document)
        response = Response[WrappedData[World]](data=result)
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except AssertionError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail="document id mismatch") from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
    return response


@router.post("/world/{world_id}")
async def world_post(world_id: str, document: World) -> Response[WrappedData[World]]:
    try:
        assert world_id == document.id
        address: Address = Address(world_id=world_id)
        result: dict = await ContextManager.daoservice.post(address=address, document=document)
        response = Response[WrappedData[World]](data=result)
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except AssertionError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail="document id mismatch") from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
    return response


@router.put("/world/{world_id}")
async def world_put(world_id: str, wrapped_document: WrappedData[World]) -> Response[WrappedData[World]]:
    try:
        assert world_id == wrapped_document.data.id
        address: Address = Address(world_id=world_id)
        result: dict = await ContextManager.daoservice.put(address=address, wrapped_document=wrapped_document)
        response = Response[WrappedData[World]](data=result)
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except AssertionError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail="document id mismatch") from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
    return response


########################################################
### /dao/world/{world_id}/chunk/{chunk_id}
########################################################


@router.get("/world/{world_id}/chunk/{chunk_id}")
async def chunk_get(world_id: str, chunk_id: str, full: bool = False) -> Response[WrappedData[Chunk]]:
    try:
        request: DocumentRequest = DocumentRequest(address=Address(world_id=world_id, chunk_id=chunk_id), full=full)
        wrapped_document: dict = await ContextManager.daoservice.get(request=request)
        response = Response[WrappedData[Chunk]](data=wrapped_document)
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
    return response


@router.delete("/world/{world_id}/chunk/{chunk_id}")
async def chunk_delete(world_id: str, chunk_id: str) -> Response[bool]:
    try:
        request: DocumentRequest = DocumentRequest(address=Address(world_id=world_id, chunk_id=chunk_id))
        success: bool = await ContextManager.daoservice.delete(request=request)
        response = Response[bool](data=success)
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
    return response


@router.patch("/world/{world_id}/chunk/{chunk_id}")
async def chunk_patch(world_id: str, chunk_id: str, document: dict) -> Response[WrappedData[Chunk]]:
    try:
        if "id" in document:
            assert chunk_id == document["id"]
        address: Address = Address(world_id=world_id, chunk_id=chunk_id)
        result: dict = await ContextManager.daoservice.patch(address=address, document=document)
        response = Response[WrappedData[Chunk]](data=result)
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except AssertionError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail="document id mismatch") from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
    return response


@router.post("/world/{world_id}/chunk/{chunk_id}")
async def chunk_post(world_id: str, chunk_id: str, document: Chunk) -> Response[WrappedData[Chunk]]:
    try:
        assert chunk_id == document.id
        address: Address = Address(world_id=world_id, chunk_id=chunk_id)
        result: dict = await ContextManager.daoservice.post(address=address, document=document)
        response = Response[WrappedData[Chunk]](data=result)
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except AssertionError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail="document id mismatch") from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
    return response


@router.put("/world/{world_id}/chunk/{chunk_id}")
async def chunk_put(world_id: str, chunk_id: str, wrapped_document: WrappedData[Chunk]) -> Response[WrappedData[Chunk]]:
    try:
        assert chunk_id == wrapped_document.data.id
        address: Address = Address(world_id=world_id, chunk_id=chunk_id)
        result: dict = await ContextManager.daoservice.put(address=address, wrapped_document=wrapped_document)
        response = Response[WrappedData[Chunk]](data=result)
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except AssertionError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail="document id mismatch") from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
    return response


########################################################
### /dao/world/{world_id}/chunk/{chunk_id}/tile/{tile_id}
########################################################


@router.get("/world/{world_id}/chunk/{chunk_id}/tile/{tile_id}")
async def tile_get(world_id: str, chunk_id: str, tile_id: str, full: bool = False) -> Response[WrappedData[Tile]]:
    try:
        request: DocumentRequest = DocumentRequest(
            address=Address(world_id=world_id, chunk_id=chunk_id, tile_id=tile_id), full=full
        )
        wrapped_document: dict = await ContextManager.daoservice.get(request=request)
        response = Response[WrappedData[Tile]](data=wrapped_document)
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
    return response


@router.delete("/world/{world_id}/chunk/{chunk_id}/tile/{tile_id}")
async def tile_delete(world_id: str, chunk_id: str, tile_id: str) -> Response[bool]:
    try:
        request: DocumentRequest = DocumentRequest(
            address=Address(world_id=world_id, chunk_id=chunk_id, tile_id=tile_id)
        )
        success: bool = await ContextManager.daoservice.delete(request=request)
        response = Response[bool](data=success)
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
    return response


@router.patch("/world/{world_id}/chunk/{chunk_id}/tile/{tile_id}")
async def tile_patch(world_id: str, chunk_id: str, tile_id: str, document: dict) -> Response[WrappedData[Tile]]:
    try:
        if "id" in document:
            assert tile_id == document["id"]
        address: Address = Address(world_id=world_id, chunk_id=chunk_id, tile_id=tile_id)
        result: dict = await ContextManager.daoservice.patch(address=address, document=document)
        response = Response[WrappedData[Tile]](data=result)
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except AssertionError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail="document id mismatch") from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
    return response


@router.post("/world/{world_id}/chunk/{chunk_id}/tile/{tile_id}")
async def tile_post(world_id: str, chunk_id: str, tile_id: str, document: Tile) -> Response[WrappedData[Tile]]:
    try:
        assert tile_id == document.id
        address: Address = Address(world_id=world_id, chunk_id=chunk_id, tile_id=tile_id)
        result: dict = await ContextManager.daoservice.post(address=address, document=document)
        response = Response[WrappedData[Tile]](data=result)
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except AssertionError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail="document id mismatch") from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
    return response


@router.put("/world/{world_id}/chunk/{chunk_id}/tile/{tile_id}")
async def tile_put(
    world_id: str, chunk_id: str, tile_id: str, wrapped_document: WrappedData[Tile]
) -> Response[WrappedData[Tile]]:
    try:
        assert tile_id == wrapped_document.data.id
        address: Address = Address(world_id=world_id, chunk_id=chunk_id, tile_id=tile_id)
        result: dict = await ContextManager.daoservice.put(address=address, wrapped_document=wrapped_document)
        response = Response[WrappedData[Tile]](data=result)
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except AssertionError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail="document id mismatch") from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
    return response


########################################################
### /dao/world/{world_id}/chunk/{chunk_id}/tile/{tile_id}/entity/{entity_id}
########################################################


@router.get("/world/{world_id}/chunk/{chunk_id}/tile/{tile_id}/entity/{entity_id}")
async def entity_get(
    world_id: str, chunk_id: str, tile_id: str, entity_id: str, full: bool = False
) -> Response[WrappedData[Entity]]:
    try:
        request: DocumentRequest = DocumentRequest(
            address=Address(world_id=world_id, chunk_id=chunk_id, tile_id=tile_id, entity_id=entity_id), full=full
        )
        wrapped_document: dict = await ContextManager.daoservice.get(request=request)
        response = Response[WrappedData[Entity]](data=wrapped_document)
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
    return response


@router.delete("/world/{world_id}/chunk/{chunk_id}/tile/{tile_id}/entity/{entity_id}")
async def entity_delete(world_id: str, chunk_id: str, tile_id: str, entity_id: str) -> Response[bool]:
    try:
        request: DocumentRequest = DocumentRequest(
            address=Address(world_id=world_id, chunk_id=chunk_id, tile_id=tile_id, entity_id=entity_id)
        )
        success: bool = await ContextManager.daoservice.delete(request=request)
        response = Response[bool](data=success)
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
    return response


@router.patch("/world/{world_id}/chunk/{chunk_id}/tile/{tile_id}/entity/{entity_id}")
async def entity_patch(
    world_id: str, chunk_id: str, tile_id: str, entity_id: str, document: dict
) -> Response[WrappedData[Entity]]:
    try:
        if "id" in document:
            assert entity_id == document["id"]
        address: Address = Address(world_id=world_id, chunk_id=chunk_id, tile_id=tile_id, entity_id=entity_id)
        result: dict = await ContextManager.daoservice.patch(address=address, document=document)
        response = Response[WrappedData[Entity]](data=result)
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except AssertionError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail="document id mismatch") from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
    return response


@router.post("/world/{world_id}/chunk/{chunk_id}/tile/{tile_id}/entity/{entity_id}")
async def entity_post(
    world_id: str, chunk_id: str, tile_id: str, entity_id: str, document: Entity
) -> Response[WrappedData[Entity]]:
    try:
        assert entity_id == document.id
        address: Address = Address(world_id=world_id, chunk_id=chunk_id, tile_id=tile_id, entity_id=entity_id)
        result: dict = await ContextManager.daoservice.post(address=address, document=document)
        response = Response[WrappedData[Entity]](data=result)
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except AssertionError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail="document id mismatch") from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
    return response


@router.put("/world/{world_id}/chunk/{chunk_id}/tile/{tile_id}/entity/{entity_id}")
async def entity_put(
    world_id: str, chunk_id: str, tile_id: str, entity_id: str, wrapped_document: WrappedData[Entity]
) -> Response[WrappedData[Entity]]:
    try:
        assert entity_id == wrapped_document.data.id
        address: Address = Address(world_id=world_id, chunk_id=chunk_id, tile_id=tile_id, entity_id=entity_id)
        result: dict = await ContextManager.daoservice.put(address=address, wrapped_document=wrapped_document)
        response = Response[WrappedData[Entity]](data=result)
    except DaoConflictError as error:
        logger.error(str(error))
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DaoDoesNotExistError as error:
        logger.error(str(error))
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DaoInconsistencyError as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error)) from error
    except AssertionError as error:
        logger.error(str(error))
        raise HTTPException(status_code=400, detail="document id mismatch") from error
    except Exception as error:
        traceback.print_exc()
        logger.error(str(error))
        # catch everything else
        raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
    return response
