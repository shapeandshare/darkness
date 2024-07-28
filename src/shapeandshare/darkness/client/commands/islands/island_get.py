import requests

from ....contracts.dtos.island import Island
from ....contracts.dtos.requests.island_get_request import IslandGetRequest
from ....contracts.dtos.responses.response import Response
from ..abstract import AbstractCommand


class IslandGetCommand(AbstractCommand):
    def execute(self, request: IslandGetRequest) -> Island:
        response: requests.Response = requests.get(
            url=f"http://{self.options.tld}/island/{request.id}",
            timeout=self.options.timeout,
            json=request.model_dump(),
        )
        return Response[Island].model_validate(response.json()).data
