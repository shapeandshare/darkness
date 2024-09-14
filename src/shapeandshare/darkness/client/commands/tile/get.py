""" Tile Get Command """

import requests

from ....sdk.contracts.dtos.sdk.requests.tile.get import TileGetRequest
from ....sdk.contracts.dtos.sdk.responses.chunk.get import ChunkGetResponse
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ..abstract import AbstractCommand


class TileGetCommand(AbstractCommand):
    async def execute(self, request: TileGetRequest) -> ChunkGetResponse:
        response: requests.Response = requests.get(
            url=f"http://{self.options.tld}/world/{request.world_id}/chunk/{request.chunk_id}/tile/{request.tile_id}",
            timeout=self.options.timeout,
            params={"full": request.full},
        )
        return Response[ChunkGetResponse].model_validate(response.json()).data
