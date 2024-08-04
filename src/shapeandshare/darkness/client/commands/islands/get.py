import requests

from ....sdk.contracts.dtos.sdk.responses.islands.get import IslandsGetResponse
from ....sdk.contracts.dtos.sdk.responses.response import Response
from ..abstract import AbstractCommand


class IslandsGetCommand(AbstractCommand):
    def execute(self) -> IslandsGetResponse:
        response: requests.Response = requests.get(
            url=f"http://{self.options.tld}/islands", timeout=self.options.timeout
        )
        return Response[IslandsGetResponse].model_validate(response.json()).data
