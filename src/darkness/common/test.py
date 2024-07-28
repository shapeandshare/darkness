from ..client.client import Client

client = Client()

response = client.health_get()
print(response)
