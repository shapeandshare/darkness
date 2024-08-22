from ..sdk.common.utils import address_type
from ..sdk.contracts.dtos.entities.entity import Entity
from ..sdk.contracts.dtos.sdk.command_options import CommandOptions
from ..sdk.contracts.dtos.sdk.requests.document.document import DocumentRequest
from ..sdk.contracts.dtos.sdk.requests.document.patch import DocumentPatchRequest
from ..sdk.contracts.dtos.sdk.requests.document.post import DocumentPostRequest
from ..sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ..sdk.contracts.dtos.tiles.address import Address
from ..sdk.contracts.dtos.tiles.chunk import Chunk
from ..sdk.contracts.dtos.tiles.tile import Tile
from ..sdk.contracts.dtos.tiles.world import World
from ..sdk.contracts.types.dao_document import DaoDocumentType
from .commands.document.delete import DocumentDeleteCommand
from .commands.document.get import DocumentGetCommand
from .commands.document.patch import DocumentPatchCommand
from .commands.document.post import DocumentPostCommand
from .commands.document.put import DocumentPutCommand
from .commands.metrics.health.get import HealthGetCommand


class DaoClient:
    # metrics/health
    health_get_command: HealthGetCommand

    # dao/
    document_get_command: DocumentGetCommand
    document_put_command: DocumentPutCommand
    document_patch_command: DocumentPatchCommand
    document_post_command: DocumentPostCommand
    document_delete_command: DocumentDeleteCommand

    def __init__(self, options: CommandOptions | None = None):
        command_dict: dict = {}
        if options:
            command_dict["options"] = options

        ### metrics
        self.health_get_command = HealthGetCommand.model_validate(command_dict)

        ### dao
        self.document_get_command = DocumentGetCommand.model_validate(command_dict)
        self.document_put_command = DocumentPutCommand.model_validate(command_dict)
        self.document_patch_command = DocumentPatchCommand.model_validate(command_dict)
        self.document_post_command = DocumentPostCommand.model_validate(command_dict)
        self.document_delete_command = DocumentDeleteCommand.model_validate(command_dict)

    async def health_get(self) -> dict:
        """
        Gets the server health.

        Returns
        -------
        health: dict
            The server health (true or false).
        """

        return await self.health_get_command.execute()

    async def document_delete(self, address: Address) -> bool:
        request: DocumentRequest = DocumentRequest(address=address)
        response = await self.document_delete_command.execute(request)
        return response.data

    async def document_get(
        self, address: Address, full: bool
    ) -> WrappedData[World] | WrappedData[Chunk] | WrappedData[Tile] | WrappedData[Entity]:
        request: DocumentRequest = DocumentRequest(address=address, full=full)
        doc_type: DaoDocumentType = address_type(address=request.address)

        response = await self.document_get_command.execute(request=request)

        if doc_type == DaoDocumentType.WORLD:
            return WrappedData[World].model_validate(response.data)
        elif doc_type == DaoDocumentType.CHUNK:
            return WrappedData[Chunk].model_validate(response.data)
        elif doc_type == DaoDocumentType.TILE:
            return WrappedData[Tile].model_validate(response.data)
        elif doc_type == DaoDocumentType.ENTITY:
            return WrappedData[Entity].model_validate(response.data)
        raise Exception("Unknown document requested")

    async def document_patch(
        self, address: Address, document: dict
    ) -> WrappedData[World] | WrappedData[Chunk] | WrappedData[Tile] | WrappedData[Entity]:
        request: DocumentPatchRequest = DocumentPatchRequest(address=address, document=document)
        doc_type: DaoDocumentType = address_type(address=request.address)

        response = await self.document_patch_command.execute(request)

        if doc_type == DaoDocumentType.WORLD:
            return WrappedData[World].model_validate(response.data)
        elif doc_type == DaoDocumentType.CHUNK:
            return WrappedData[Chunk].model_validate(response.data)
        elif doc_type == DaoDocumentType.TILE:
            return WrappedData[Tile].model_validate(response.data)
        elif doc_type == DaoDocumentType.ENTITY:
            return WrappedData[Entity].model_validate(response.data)
        raise Exception("Unknown document requested")

    async def document_post(
        self, address: Address, document: World | Chunk | Tile | Entity
    ) -> WrappedData[World] | WrappedData[Chunk] | WrappedData[Tile] | WrappedData[Entity]:
        doc_type: DaoDocumentType = address_type(address=address)

        if doc_type == DaoDocumentType.WORLD:
            request: DocumentPostRequest[World] = DocumentPostRequest[World](address=address, document=document)
        elif doc_type == DaoDocumentType.CHUNK:
            request: DocumentPostRequest[Chunk] = DocumentPostRequest[Chunk](address=address, document=document)
        elif doc_type == DaoDocumentType.TILE:
            request: DocumentPostRequest[Tile] = DocumentPostRequest[Tile](address=address, document=document)
        elif doc_type == DaoDocumentType.ENTITY:
            request: DocumentPostRequest[Entity] = DocumentPostRequest[Entity](address=address, document=document)
        else:
            raise Exception("Unknown document requested")

        response = await self.document_post_command.execute(request=request)

        if doc_type == DaoDocumentType.WORLD:
            return WrappedData[World].model_validate(response.data)
        elif doc_type == DaoDocumentType.CHUNK:
            return WrappedData[Chunk].model_validate(response.data)
        elif doc_type == DaoDocumentType.TILE:
            return WrappedData[Tile].model_validate(response.data)
        elif doc_type == DaoDocumentType.ENTITY:
            return WrappedData[Entity].model_validate(response.data)
        raise Exception("Unknown document requested")
