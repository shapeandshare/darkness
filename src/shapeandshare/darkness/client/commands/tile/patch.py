""" Tile Patch Command """

import requests

from ....sdk.contracts.dtos.sdk.requests.tile.patch import TilePatchRequest
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ..abstract import AbstractCommand


class TilePatchCommand(AbstractCommand):
    async def execute(self, request: TilePatchRequest) -> bool:
        response: requests.Response = requests.patch(
            url=f"http://{self.options.tld}/world/{request.world_id}/chunk/{request.chunk_id}/tile/{request.tile_id}",
            timeout=self.options.timeout,
            json=request.model_dump()["partial"],
        )
        return Response[bool].model_validate(response.json()).data
