import requests

from ....contracts.dtos.requests.island_delete_request import IslandDeleteRequest
from ....contracts.dtos.responses.island_delete_response import IslandDeleteResponse
from ....contracts.dtos.responses.response import Response
from ..abstract import AbstractCommand


class IslandDeleteCommand(AbstractCommand):
    def execute(self, request: IslandDeleteRequest) -> IslandDeleteResponse:
        response: requests.Response = requests.delete(
            url=f"http://{self.options.tld}/island/{request.id}", timeout=self.options.timeout
        )
        return Response[IslandDeleteResponse].model_validate(response.json()).data
