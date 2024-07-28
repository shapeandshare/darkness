import requests

from ....contracts.dtos.requests.island_create_request import IslandCreateRequest
from ....contracts.dtos.responses.island_create_response import IslandCreateResponse
from ....contracts.dtos.responses.response import Response
from ..abstract import AbstractCommand


class IslandCreateCommand(AbstractCommand):
    def execute(self, request: IslandCreateRequest) -> IslandCreateResponse:
        response: requests.Response = requests.post(
            url=f"http://{self.options.tld}/island/create",
            timeout=self.options.timeout,
            json=request.dict(),
        )
        return Response[IslandCreateResponse].parse_obj(response.json()).data
