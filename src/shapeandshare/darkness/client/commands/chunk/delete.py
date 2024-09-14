""" Chunk Delete Command """

import requests

from ....sdk.contracts.dtos.sdk.requests.chunk.delete import ChunkDeleteRequest
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ..abstract import AbstractCommand


class ChunkDeleteCommand(AbstractCommand):
    async def execute(self, request: ChunkDeleteRequest) -> bool:
        response: requests.Response = requests.delete(
            url=f"http://{self.options.tld}/world/{request.world_id}/chunk/{request.chunk_id}",
            timeout=self.options.timeout,
            params={"parent": request.parent, "cascade": request.cascade},
        )
        return Response[bool].model_validate(response.json()).data
