# from ..client.client import Client
from shapeandshare.darkness import Client

client = Client()

response = client.health_get()
print(response)

island_id = client.island_create(dim=[50, 50], biome="dirt")
print(island_id)


island = client.island_get(id=island_id)
print(island.model_dump_json(indent=4))
