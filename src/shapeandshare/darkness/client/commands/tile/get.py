""" Tile Get Command """

import requests

from ....sdk.contracts.dtos.sdk.requests.tile.get import TileGetRequest
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ....sdk.contracts.dtos.sdk.responses.tile.get import TileGetResponse
from ..abstract import AbstractCommand


class TileGetCommand(AbstractCommand):
    async def execute(self, request: TileGetRequest) -> TileGetResponse:
        response: requests.Response = requests.get(
            url=f"http://{self.options.tld}/world/{request.world_id}/chunk/{request.chunk_id}/tile/{request.tile_id}",
            timeout=self.options.timeout,
            params={"full": request.full},
        )
        return Response[TileGetResponse].model_validate(response.json()).data
