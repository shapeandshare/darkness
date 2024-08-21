from pydantic import BaseModel

from ...sdk.contracts.dtos.entities.entity import Entity
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

    @staticmethod
    def address_type(address: Address) -> DaoDocumentType:
        if address.entity_id is not None:
            return DaoDocumentType.ENTITY
        elif address.tile_id is not None:
            return DaoDocumentType.TILE
        elif address.chunk_id is not None:
            return DaoDocumentType.CHUNK
        elif address.world_id is not None:
            return DaoDocumentType.WORLD

        raise Exception("Unknown address type")

    async def get(
        self, address: Address
    ) -> WrappedData[World] | WrappedData[Chunk] | WrappedData[Tile] | WrappedData[Entity]:
        document_type: DaoDocumentType = DaoService.address_type(address)
        if document_type == DaoDocumentType.TILE:
            wrapped_document: WrappedData[Tile] = await self.tiledao.get(address=address)
            wrapped_document.data = Tile.model_validate(wrapped_document.data)
            return wrapped_document

        if document_type == DaoDocumentType.ENTITY:
            wrapped_document: WrappedData[Entity] = await self.entitydao.get(address=address)
            wrapped_document.data = Entity.model_validate(wrapped_document.data)
            return wrapped_document

        if document_type == DaoDocumentType.CHUNK:
            wrapped_document: WrappedData[Chunk] = await self.chunkdao.get(address=address)
            wrapped_document.data = Chunk.model_validate(wrapped_document.data)
            return wrapped_document

        if document_type == DaoDocumentType.WORLD:
            wrapped_document: WrappedData[World] = await self.worlddao.get(address=address)
            wrapped_document.data = World.model_validate(wrapped_document.data)
            return wrapped_document

    async def delete(self, address: Address) -> bool:
        document_type: DaoDocumentType = DaoService.address_type(address)

        if document_type == DaoDocumentType.TILE:
            return await self.tiledao.delete(address=address)

        if document_type == DaoDocumentType.ENTITY:
            return await self.entitydao.delete(address=address)

        if document_type == DaoDocumentType.CHUNK:
            return await self.chunkdao.delete(address=address)

        if document_type == DaoDocumentType.WORLD:
            return await self.worlddao.delete(address=address)

    async def patch(
        self, address: Address, document: dict, exclude: dict | None = None
    ) -> WrappedData[World] | WrappedData[Chunk] | WrappedData[Tile] | WrappedData[Entity]:
        document_type: DaoDocumentType = DaoService.address_type(address)

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
        document_type: DaoDocumentType = DaoService.address_type(address)

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
        document_type: DaoDocumentType = DaoService.address_type(address)

        if document_type == DaoDocumentType.TILE:
            return await self.tiledao.put(address=address, wrapped_document=wrapped_document, exclude=exclude)

        if document_type == DaoDocumentType.ENTITY:
            return await self.entitydao.put(address=address, wrapped_document=wrapped_document, exclude=exclude)

        if document_type == DaoDocumentType.CHUNK:
            return await self.chunkdao.put(address=address, wrapped_document=wrapped_document, exclude=exclude)

        if document_type == DaoDocumentType.WORLD:
            return await self.worlddao.put(address=address, wrapped_document=wrapped_document, exclude=exclude)
