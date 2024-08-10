import requests

from ....sdk.contracts.dtos.sdk.requests.world.get import WorldGetRequest
from ....sdk.contracts.dtos.sdk.responses.islands.get import IslandsGetResponse
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ....sdk.contracts.dtos.sdk.responses.world.get import WorldGetResponse
from ..abstract import AbstractCommand


class WorldGetCommand(AbstractCommand):
    def execute(self, request: WorldGetRequest) -> WorldGetResponse:
        response: requests.Response = requests.get(
            url=f"http://{self.options.tld}/world/{request.id}", timeout=self.options.timeout
        )
        return Response[WorldGetResponse].model_validate(response.json()).data
