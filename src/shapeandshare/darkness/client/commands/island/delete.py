import requests

from ....sdk.contracts.dtos.sdk.requests.island.delete import IslandDeleteRequest
from ....sdk.contracts.dtos.sdk.responses.island.delete import IslandDeleteResponse
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ..abstract import AbstractCommand


class IslandDeleteCommand(AbstractCommand):
    async def execute(self, request: IslandDeleteRequest) -> IslandDeleteResponse:
        response: requests.Response = requests.delete(
            url=f"http://{self.options.tld}/world/{request.world_id}/island/{request.island_id}",
            timeout=self.options.timeout,
        )
        return Response[IslandDeleteResponse].model_validate(response.json()).data
