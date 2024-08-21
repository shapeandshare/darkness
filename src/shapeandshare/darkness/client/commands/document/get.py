# import requests
#
# from ....sdk.contracts.dtos.sdk.requests.document.document import DocumentRequest
# from ....sdk.contracts.dtos.sdk.responses.response import Response
# from ..abstract import AbstractCommand
#
#
# class DocumentGetCommand(AbstractCommand):
#     async def execute(self, request: DocumentRequest) -> DocumentGetResponse:
#         response: requests.Response = requests.get(
#             url=f"http://{self.options.tld}/world/{request.world_id}/chunk/{request.chunk_id}",
#             timeout=self.options.timeout,
#             params={"full": request.full},
#         )
#         return Response[DocumentGetResponse].model_validate(response.json()).data
