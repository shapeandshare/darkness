""" Tile Delete Command """

import requests

from ....sdk.contracts.dtos.sdk.requests.tile.delete import TileDeleteRequest
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ..abstract import AbstractCommand


class TileDeleteCommand(AbstractCommand):
    async def execute(self, request: TileDeleteRequest) -> bool:
        response: requests.Response = requests.delete(
            url=f"http://{self.options.tld}/world/{request.world_id}/chunk/{request.chunk_id}/tile/{request.tile_id}",
            timeout=self.options.timeout,
            params={"parent": request.parent, "cascade": request.cascade},
        )
        return Response[bool].model_validate(response.json()).data
