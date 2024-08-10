import requests

from ....sdk.contracts.dtos.sdk.requests.island.create import IslandCreateRequest
from ....sdk.contracts.dtos.sdk.responses.island.create import IslandCreateResponse
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ..abstract import AbstractCommand


class IslandCreateCommand(AbstractCommand):
    def execute(self, request: IslandCreateRequest) -> IslandCreateResponse:
        response: requests.Response = requests.post(
            url=f"http://{self.options.tld}/world/{request.world_id}/island",
            timeout=self.options.timeout,
            json=request.model_dump(),
        )
        return Response[IslandCreateResponse].model_validate(response.json()).data
