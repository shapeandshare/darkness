import requests

from ....contracts.dtos.responses.islands_get_response import IslandsGetResponse
from ....contracts.dtos.responses.response import Response
from ..abstract import AbstractCommand


class IslandsGetCommand(AbstractCommand):
    def execute(self) -> IslandsGetResponse:
        response: requests.Response = requests.get(
            url=f"http://{self.options.tld}/islands", timeout=self.options.timeout
        )
        return Response[IslandsGetResponse].model_validate(response.json()).data
