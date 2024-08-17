import requests

from ....sdk.contracts.dtos.sdk.requests.chunk.create import ChunkCreateRequest
from ....sdk.contracts.dtos.sdk.responses.chunk.create import ChunkCreateResponse
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ..abstract import AbstractCommand


class ChunkCreateCommand(AbstractCommand):
    async def execute(self, request: ChunkCreateRequest) -> ChunkCreateResponse:
        response: requests.Response = requests.post(
            url=f"http://{self.options.tld}/world/{request.world_id}/chunk",
            timeout=self.options.timeout,
            json=request.model_dump(),
        )
        return Response[ChunkCreateResponse].model_validate(response.json()).data
