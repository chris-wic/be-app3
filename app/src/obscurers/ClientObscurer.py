from app.src.obscurers.ClientObscurerInterface import ClientObscurerInterface
from app.src.models import ToBeObscuredClient


class ClientObscurer(ClientObscurerInterface):
    def obscure_client(self, client: ToBeObscuredClient) -> ToBeObscuredClient:

        client.first_name = "x" * len(client.first_name)
        client.last_name = "x" * len(client.last_name)
        client.phone = "x" * len(client.phone)

        # Obscure email while preserving dots in domain
        local_part, domain = client.email.split("@")
        # Replace characters in domain with asterisks but keep dots
        obscured_domain = "".join("x" if char != "." else "." for char in domain)
        client.email = "x" * len(local_part) + "@" + obscured_domain
        client.is_obscured = True

        return client