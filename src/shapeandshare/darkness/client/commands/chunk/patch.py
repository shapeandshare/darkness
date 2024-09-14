""" Chunk Create Command """

import requests

from ....sdk.contracts.dtos.sdk.requests.chunk.patch import ChunkPatchRequest
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ..abstract import AbstractCommand


class ChunkPatchCommand(AbstractCommand):
    async def execute(self, request: ChunkPatchRequest) -> bool:
        response: requests.Response = requests.patch(
            url=f"http://{self.options.tld}/world/{request.world_id}/chunk/{request.chunk_id}",
            timeout=self.options.timeout,
            json=request.model_dump()["partial"],
        )
        return Response[bool].model_validate(response.json()).data
