from app.src.obscurers.ClientObscurerInterface import ClientObscurerInterface
from app.src.models import ToBeObscuredClient

class ClientStrongObscurer(ClientObscurerInterface):
    def obscure_client(self, client: ToBeObscuredClient) -> ToBeObscuredClient:
        client.first_name = "X" * len(client.first_name)
        client.last_name = "X" * len(client.last_name)
        client.phone = "X" * len(client.phone)
        client.email = "X" * len(client.email)
        return client