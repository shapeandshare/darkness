# import logging
# import traceback
#
# from fastapi import APIRouter, HTTPException
#
# from .....sdk.contracts.dtos.sdk.requests.chunk.create import ChunkCreateRequest
# from .....sdk.contracts.dtos.sdk.requests.chunk.delete import ChunkDeleteRequest
# from .....sdk.contracts.dtos.sdk.requests.chunk.get import ChunkGetRequest
# from .....sdk.contracts.dtos.sdk.requests.world.create import WorldCreateRequest
# from .....sdk.contracts.dtos.sdk.requests.world.delete import WorldDeleteRequest
# from .....sdk.contracts.dtos.sdk.requests.world.get import WorldGetRequest
# from .....sdk.contracts.dtos.sdk.responses.chunk.create import ChunkCreateResponse
# from .....sdk.contracts.dtos.sdk.responses.chunk.get import ChunkGetResponse
# from .....sdk.contracts.dtos.sdk.responses.response import Response
# from .....sdk.contracts.dtos.sdk.responses.world.create import WorldCreateResponse
# from .....sdk.contracts.dtos.sdk.responses.world.get import WorldGetResponse
# from .....sdk.contracts.dtos.tiles.chunk import Chunk
# from .....sdk.contracts.dtos.tiles.world import World
# from .....sdk.contracts.errors.server.dao.conflict import DaoConflictError
# from .....sdk.contracts.errors.server.dao.doesnotexist import DaoDoesNotExistError
# from .....sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError
# from ..context import ContextManager
#
# # from pyinstrument import Profiler
#
#
# logger = logging.getLogger()
#
# router: APIRouter = APIRouter(
#     prefix="/dao",
#     tags=["dao"],
# )
#
#
# ### /dao
#
#
# @router.get("/{document_id}")
# async def world_get(document_id: str, full: bool = False) -> Response[DocumentGetResponse]:
#     request: DocumentGetRequest = DocumentGetRequest(id=document_id)
#
#     try:
#         if full:
#             document: World = await ContextManager.state_service.world_get(request=request)
#             response = Response[DocumentGetResponse](data=DocumentGetResponse(document=document))
#         else:
#             document_lite: World = await ContextManager.state_service.world_lite_get(request=request)
#             response = Response[DocumentGetResponse](data=DocumentGetResponse(document=document_lite))
#     except DaoConflictError as error:
#         traceback.print_exc()
#         logger.error(str(error))
#         raise HTTPException(status_code=409, detail=str(error)) from error
#     except DaoDoesNotExistError as error:
#         traceback.print_exc()
#         logger.error(str(error))
#         raise HTTPException(status_code=404, detail=str(error)) from error
#     except DaoInconsistencyError as error:
#         traceback.print_exc()
#         logger.error(str(error))
#         raise HTTPException(status_code=500, detail=str(error)) from error
#     except Exception as error:
#         traceback.print_exc()
#         logger.error(str(error))
#         # catch everything else
#         raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
#
#     return response
#
#
# #
# #
# # @router.delete("/{world_id}")
# # async def world_delete(world_id: str) -> None:
# #     request: WorldDeleteRequest = WorldDeleteRequest(id=world_id)
# #
# #     try:
# #         await ContextManager.state_service.world_delete(request=request)
# #     except DaoConflictError as error:
# #         traceback.print_exc()
# #         logger.error(str(error))
# #         raise HTTPException(status_code=409, detail=str(error)) from error
# #     except DaoDoesNotExistError as error:
# #         traceback.print_exc()
# #         logger.error(str(error))
# #         raise HTTPException(status_code=404, detail=str(error)) from error
# #     except DaoInconsistencyError as error:
# #         traceback.print_exc()
# #         logger.error(str(error))
# #         raise HTTPException(status_code=500, detail=str(error)) from error
# #     except Exception as error:
# #         traceback.print_exc()
# #         logger.error(str(error))
# #         # catch everything else
# #         raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
# #
# #
# # @router.post("")
# # async def world_create(request: WorldCreateRequest) -> Response[WorldCreateResponse]:
# #     try:
# #         world_id: str = await ContextManager.state_service.world_create(request=request)
# #     except DaoConflictError as error:
# #         traceback.print_exc()
# #         logger.error(str(error))
# #         raise HTTPException(status_code=409, detail=str(error)) from error
# #     except DaoDoesNotExistError as error:
# #         traceback.print_exc()
# #         logger.error(str(error))
# #         raise HTTPException(status_code=404, detail=str(error)) from error
# #     except DaoInconsistencyError as error:
# #         traceback.print_exc()
# #         logger.error(str(error))
# #         raise HTTPException(status_code=500, detail=str(error)) from error
# #     except Exception as error:
# #         traceback.print_exc()
# #         logger.error(str(error))
# #         # catch everything else
# #         raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
# #
# #     return Response[WorldCreateResponse](data=WorldCreateResponse(id=world_id))
# #
# #
# # ### /world/world_id/chunk/
# #
# #
# # @router.post("/{world_id}/chunk")
# # async def chunk_create(world_id: str, request: ChunkCreateRequest) -> Response[ChunkCreateResponse]:
# #     # we ignore any passed in world_ids in this condition and over-write based on path.
# #     # Due to this world_id is optional within the DTO.
# #     request.world_id = world_id
# #
# #     try:
# #         # with Profiler() as profiler:
# #         chunk_id: str = await ContextManager.state_service.chunk_create(request=request)
# #         # profiler.print()
# #     except DaoConflictError as error:
# #         traceback.print_exc()
# #         logger.error(str(error))
# #         raise HTTPException(status_code=409, detail=str(error)) from error
# #     except DaoDoesNotExistError as error:
# #         traceback.print_exc()
# #         logger.error(str(error))
# #         raise HTTPException(status_code=404, detail=str(error)) from error
# #     except DaoInconsistencyError as error:
# #         traceback.print_exc()
# #         logger.error(error)
# #         raise HTTPException(status_code=500, detail=str(error)) from error
# #     except Exception as error:
# #         traceback.print_exc()
# #         logger.error(str(error))
# #         # catch everything else
# #         raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
# #
# #     return Response[ChunkCreateResponse](data=ChunkCreateResponse(id=chunk_id))
# #
# #
# # @router.get("/{world_id}/chunk/{chunk_id}")
# # async def chunk_get(world_id: str, chunk_id: str, full: bool = True) -> Response[ChunkGetResponse]:
# #     request: ChunkGetRequest = ChunkGetRequest(world_id=world_id, chunk_id=chunk_id)
# #
# #     try:
# #         if full:
# #             chunk: Chunk = await ContextManager.state_service.chunk_get(request=request)
# #             response = Response[ChunkGetResponse](data=ChunkGetResponse(chunk=chunk))
# #         else:
# #             chunk: Chunk = await ContextManager.state_service.chunk_lite_get(request=request)
# #             response = Response[ChunkGetResponse](data=ChunkGetResponse(chunk=chunk))
# #     except DaoConflictError as error:
# #         traceback.print_exc()
# #         logger.error(str(error))
# #         raise HTTPException(status_code=409, detail=str(error)) from error
# #     except DaoDoesNotExistError as error:
# #         traceback.print_exc()
# #         logger.error(str(error))
# #         raise HTTPException(status_code=404, detail=str(error)) from error
# #     except DaoInconsistencyError as error:
# #         traceback.print_exc()
# #         logger.error(str(error))
# #         raise HTTPException(status_code=500, detail=str(error)) from error
# #     except Exception as error:
# #         traceback.print_exc()
# #         logger.error(str(error))
# #         traceback.print_exc()
# #         raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
# #
# #     return response
# #
# #
# # @router.delete("/{world_id}/chunk/{chunk_id}")
# # async def chunk_delete(world_id: str, chunk_id: str) -> None:
# #     request: ChunkDeleteRequest = ChunkDeleteRequest(world_id=world_id, chunk_id=chunk_id)
# #     try:
# #         await ContextManager.state_service.chunk_delete(request=request)
# #     except DaoConflictError as error:
# #         traceback.print_exc()
# #         logger.error(str(error))
# #         raise HTTPException(status_code=409, detail=str(error)) from error
# #     except DaoDoesNotExistError as error:
# #         traceback.print_exc()
# #         logger.error(str(error))
# #         raise HTTPException(status_code=404, detail=str(error)) from error
# #     except DaoInconsistencyError as error:
# #         traceback.print_exc()
# #         logger.error(str(error))
# #         raise HTTPException(status_code=500, detail=str(error)) from error
# #     except Exception as error:
# #         traceback.print_exc()
# #         logger.error(str(error))
# #         # catch everything else
# #         raise HTTPException(status_code=500, detail=f"Uncaught exception: {str(error)}") from error
