from ..client.client import Client

client = Client()

response = client.health_get()
print(response)

response = client.island_create(dim=[50, 50], biome="dirt")
print(response)
