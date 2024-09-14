""" Entity Get Command """

import requests

from ....sdk.contracts.dtos.sdk.requests.entity.entity import EntityRequest
from ....sdk.contracts.dtos.sdk.responses.entity.get import EntityGetResponse
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ..abstract import AbstractCommand


class EntityGetCommand(AbstractCommand):
    async def execute(self, request: EntityRequest) -> EntityGetResponse:
        response: requests.Response = requests.get(
            url=f"http://{self.options.tld}/world/{request.world_id}/chunk/{request.chunk_id}/tile/{request.tile_id}/entity/{request.entity_id}",
            timeout=self.options.timeout,
        )
        return Response[EntityGetResponse].model_validate(response.json()).data
