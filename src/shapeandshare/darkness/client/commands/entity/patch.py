""" Entity Patch Command """

import requests

from ....sdk.contracts.dtos.sdk.requests.entity.patch import EntityPatchRequest
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ..abstract import AbstractCommand


class EntityPatchCommand(AbstractCommand):
    async def execute(self, request: EntityPatchRequest) -> bool:
        response: requests.Response = requests.patch(
            url=f"http://{self.options.tld}/world/{request.world_id}/chunk/{request.chunk_id}/tile/{request.tile_id}/entity/{request.entity_id}",
            timeout=self.options.timeout,
            json=request.model_dump()["partial"],
        )
        return Response[bool].model_validate(response.json()).data
