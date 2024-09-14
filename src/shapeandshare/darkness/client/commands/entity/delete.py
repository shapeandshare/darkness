""" Entity Delete Command """

import requests

from ....sdk.contracts.dtos.sdk.requests.entity.delete import EntityDeleteRequest
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ..abstract import AbstractCommand


class EntityDeleteCommand(AbstractCommand):
    async def execute(self, request: EntityDeleteRequest) -> bool:
        response: requests.Response = requests.delete(
            url=f"http://{self.options.tld}/world/{request.world_id}/chunk/{request.chunk_id}/tile/{request.tile_id}/entity/{request.entity_id}",
            timeout=self.options.timeout,
            params={"parent": request.parent},
        )
        return Response[bool].model_validate(response.json()).data
