import requests

from ....sdk.common.utils import address_type, document_path
from ....sdk.contracts.dtos.entities.entity import Entity
from ....sdk.contracts.dtos.sdk.requests.document.post import DocumentPostRequest
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ....sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ....sdk.contracts.dtos.tiles.chunk import Chunk
from ....sdk.contracts.dtos.tiles.tile import Tile
from ....sdk.contracts.dtos.tiles.world import World
from ....sdk.contracts.types.dao_document import DaoDocumentType
from ..abstract import AbstractCommand


class DocumentPostCommand(AbstractCommand):
    async def execute(
        self,
        request: (
            DocumentPostRequest[World]
            | DocumentPostRequest[Chunk]
            | DocumentPostRequest[Tile]
            | DocumentPostRequest[Entity]
        ),
    ) -> (
        Response[WrappedData[World]]
        | Response[WrappedData[Chunk]]
        | Response[WrappedData[Tile]]
        | Response[WrappedData[Entity]]
    ):

        doc_type: DaoDocumentType = address_type(address=request.address)
        doc_path: str = document_path(address=request.address, doc_type=doc_type)
        url: str = f"http://{self.options.tld}/dao/{doc_path}"
        response: requests.Response = requests.post(
            url=url, timeout=self.options.timeout, data=request.document.model_dump()
        )
        if doc_type == DaoDocumentType.WORLD:
            return Response[WrappedData[World]].model_validate(response.json())
        elif doc_type == DaoDocumentType.CHUNK:
            return Response[WrappedData[Chunk]].model_validate(response.json())
        elif doc_type == DaoDocumentType.TILE:
            return Response[WrappedData[Tile]].model_validate(response.json())
        elif doc_type == DaoDocumentType.ENTITY:
            return Response[WrappedData[Entity]].model_validate(response.json())
        raise Exception("Unknown document requested")
