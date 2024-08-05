import requests

from ....sdk.contracts.dtos.sdk.requests.island.get import IslandGetRequest
from ....sdk.contracts.dtos.sdk.responses.island.get import IslandGetResponse
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ..abstract import AbstractCommand


class IslandGetCommand(AbstractCommand):
    def execute(self, request: IslandGetRequest) -> IslandGetResponse:
        response: requests.Response = requests.get(
            url=f"http://{self.options.tld}/island/{request.id}", timeout=self.options.timeout
        )
        return Response[IslandGetResponse].model_validate(response.json()).data
