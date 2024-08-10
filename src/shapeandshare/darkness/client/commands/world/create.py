import requests

from ....sdk.contracts.dtos.sdk.requests.world.create import WorldCreateRequest
from ....sdk.contracts.dtos.sdk.requests.world.get import WorldGetRequest
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ....sdk.contracts.dtos.sdk.responses.world.create import WorldCreateResponse
from ....sdk.contracts.dtos.sdk.responses.world.get import WorldGetResponse
from ..abstract import AbstractCommand


class WorldCreateCommand(AbstractCommand):
    def execute(self, request: WorldCreateRequest) -> WorldCreateResponse:
        response: requests.Response = requests.post(
            url=f"http://{self.options.tld}/world",
            timeout=self.options.timeout,
            json=request.model_dump(),
        )
        return Response[WorldCreateResponse].model_validate(response.json()).data
