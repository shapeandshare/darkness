import requests

from ....sdk.contracts.dtos.sdk.requests.world.create import WorldCreateRequest
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ....sdk.contracts.dtos.sdk.responses.world.create import WorldCreateResponse
from ..abstract import AbstractCommand


class WorldCreateCommand(AbstractCommand):
    async def execute(self, request: WorldCreateRequest) -> WorldCreateResponse:
        response: requests.Response = requests.post(
            url=f"http://{self.options.tld}/world",
            timeout=self.options.timeout,
            json=request.model_dump(),
        )
        return Response[WorldCreateResponse].model_validate(response.json()).data
