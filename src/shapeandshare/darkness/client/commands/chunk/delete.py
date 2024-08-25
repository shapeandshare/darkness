import requests

from ....sdk.contracts.dtos.sdk.requests.chunk.chunk import ChunkRequest
from ....sdk.contracts.dtos.sdk.responses.chunk.delete import ChunkDeleteResponse
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ..abstract import AbstractCommand


class ChunkDeleteCommand(AbstractCommand):
    async def execute(self, request: ChunkRequest) -> ChunkDeleteResponse:
        response: requests.Response = requests.delete(
            url=f"http://{self.options.tld}/world/{request.world_id}/chunk/{request.chunk_id}",
            timeout=self.options.timeout,
        )
        return Response[ChunkDeleteResponse].model_validate(response.json()).data
