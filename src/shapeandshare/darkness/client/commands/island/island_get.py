import requests

from ....contracts.dtos.requests.island_get_request import IslandGetRequest
from ....contracts.dtos.responses.island_get_response import IslandGetResponse
from ....contracts.dtos.responses.response import Response
from ..abstract import AbstractCommand


class IslandGetCommand(AbstractCommand):
    def execute(self, request: IslandGetRequest) -> IslandGetResponse:
        response: requests.Response = requests.get(
            url=f"http://{self.options.tld}/island/{request.id}", timeout=self.options.timeout
        )
        return Response[IslandGetResponse].model_validate(response.json()).data
