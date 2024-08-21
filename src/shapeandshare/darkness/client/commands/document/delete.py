import requests

from ....sdk.common.utils import address_type, document_path
from ....sdk.contracts.dtos.sdk.requests.document.document import DocumentRequest
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ....sdk.contracts.types.dao_document import DaoDocumentType
from ..abstract import AbstractCommand


class DocumentDeleteCommand(AbstractCommand):
    async def execute(self, request: DocumentRequest) -> Response[bool]:
        doc_type: DaoDocumentType = address_type(address=request.address)
        doc_path: str = document_path(address=request.address, doc_type=doc_type)
        url: str = f"http://{self.options.tld}/dao/{doc_path}"
        response: requests.Response = requests.delete(
            url=url,
            timeout=self.options.timeout,
        )
        return Response[bool].model_validate(response.json())
