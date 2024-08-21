from pydantic import BaseModel

from ...sdk.common.utils import address_type
from ...sdk.contracts.dtos.entities.entity import Entity
from ...sdk.contracts.dtos.sdk.requests.document.document import DocumentRequest
from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.dtos.tiles.address import Address
from ...sdk.contracts.dtos.tiles.chunk import Chunk
from ...sdk.contracts.dtos.tiles.tile import Tile
from ...sdk.contracts.dtos.tiles.world import World
from ...sdk.contracts.types.dao_document import DaoDocumentType
from ..dao.tile import TileDao


class DaoService(BaseModel):
    """ """

    worlddao: TileDao[World]
    chunkdao: TileDao[Chunk]
    tiledao: TileDao[Tile]
    entitydao: TileDao[Entity]

    async def get(
        self, request: DocumentRequest
    ) -> WrappedData[World] | WrappedData[Chunk] | WrappedData[Tile] | WrappedData[Entity]:
        document_type: DaoDocumentType = address_type(request.address)

        # lite
        if request.full is False:
            if document_type == DaoDocumentType.TILE:
                wrapped_document: WrappedData[Tile] = await self.tiledao.get(address=request.address)
                wrapped_document.data = Tile.model_validate(wrapped_document.data)
                return wrapped_document

            if document_type == DaoDocumentType.ENTITY:
                wrapped_document: WrappedData[Entity] = await self.entitydao.get(address=request.address)
                wrapped_document.data = Entity.model_validate(wrapped_document.data)
                return wrapped_document

            if document_type == DaoDocumentType.CHUNK:
                wrapped_document: WrappedData[Chunk] = await self.chunkdao.get(address=request.address)
                wrapped_document.data = Chunk.model_validate(wrapped_document.data)
                return wrapped_document

            if document_type == DaoDocumentType.WORLD:
                wrapped_document: WrappedData[World] = await self.worlddao.get(address=request.address)
                wrapped_document.data = World.model_validate(wrapped_document.data)
                return wrapped_document
        else:
            # else we are `full` - get all descenents
            raise NotImplementedError("else we are `full` - get all descenents")

    async def delete(self, request: DocumentRequest) -> bool:
        document_type: DaoDocumentType = address_type(request.address)

        if document_type == DaoDocumentType.TILE:
            return await self.tiledao.delete(address=request.address)

        if document_type == DaoDocumentType.ENTITY:
            return await self.entitydao.delete(address=request.address)

        if document_type == DaoDocumentType.CHUNK:
            return await self.chunkdao.delete(address=request.address)

        if document_type == DaoDocumentType.WORLD:
            return await self.worlddao.delete(address=request.address)

    async def patch(
        self, address: Address, document: dict, exclude: dict | None = None
    ) -> WrappedData[World] | WrappedData[Chunk] | WrappedData[Tile] | WrappedData[Entity]:
        document_type: DaoDocumentType = address_type(address)

        if document_type == DaoDocumentType.TILE:
            wrapped_document: WrappedData[Tile] = await self.tiledao.patch(
                address=address, document=document, exclude=exclude
            )
            wrapped_document.data = Tile.model_validate(wrapped_document.data)
            return wrapped_document

        if document_type == DaoDocumentType.ENTITY:
            wrapped_document: WrappedData[Entity] = await self.entitydao.patch(
                address=address, document=document, exclude=exclude
            )
            wrapped_document.data = Entity.model_validate(wrapped_document.data)
            return wrapped_document

        if document_type == DaoDocumentType.CHUNK:
            wrapped_document: WrappedData[Chunk] = await self.chunkdao.patch(
                address=address, document=document, exclude=exclude
            )
            wrapped_document.data = Chunk.model_validate(wrapped_document.data)
            return wrapped_document

        if document_type == DaoDocumentType.WORLD:
            wrapped_document: WrappedData[World] = await self.worlddao.patch(
                address=address, document=document, exclude=exclude
            )
            wrapped_document.data = World.model_validate(wrapped_document.data)
            return wrapped_document

    async def post(
        self, address: Address, document: World | Chunk | Tile | Entity, exclude: dict | None = None
    ) -> WrappedData[World] | WrappedData[Chunk] | WrappedData[Tile] | WrappedData[Entity]:
        document_type: DaoDocumentType = address_type(address)

        if document_type == DaoDocumentType.TILE:
            wrapped_document: WrappedData[Tile] = await self.tiledao.post(
                address=address, document=document, exclude=exclude
            )
            wrapped_document.data = Tile.model_validate(wrapped_document.data)
            return wrapped_document

        if document_type == DaoDocumentType.ENTITY:
            wrapped_document: WrappedData[Entity] = await self.entitydao.post(
                address=address, document=document, exclude=exclude
            )
            wrapped_document.data = Entity.model_validate(wrapped_document.data)
            return wrapped_document

        if document_type == DaoDocumentType.CHUNK:
            wrapped_document: WrappedData[Chunk] = await self.chunkdao.post(
                address=address, document=document, exclude=exclude
            )
            wrapped_document.data = Chunk.model_validate(wrapped_document.data)
            return wrapped_document

        if document_type == DaoDocumentType.WORLD:
            wrapped_document: WrappedData[World] = await self.worlddao.post(
                address=address, document=document, exclude=exclude
            )
            wrapped_document.data = World.model_validate(wrapped_document.data)
            return wrapped_document

    async def put(
        self,
        address: Address,
        wrapped_document: WrappedData[World] | WrappedData[Chunk] | WrappedData[Tile] | WrappedData[Entity],
        exclude: dict | None = None,
    ) -> WrappedData[World] | WrappedData[Chunk] | WrappedData[Tile] | WrappedData[Entity]:
        document_type: DaoDocumentType = address_type(address)

        if document_type == DaoDocumentType.TILE:
            return await self.tiledao.put(address=address, wrapped_document=wrapped_document, exclude=exclude)

        if document_type == DaoDocumentType.ENTITY:
            return await self.entitydao.put(address=address, wrapped_document=wrapped_document, exclude=exclude)

        if document_type == DaoDocumentType.CHUNK:
            return await self.chunkdao.put(address=address, wrapped_document=wrapped_document, exclude=exclude)

        if document_type == DaoDocumentType.WORLD:
            return await self.worlddao.put(address=address, wrapped_document=wrapped_document, exclude=exclude)
