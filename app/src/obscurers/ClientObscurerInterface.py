from app.src.models import ToBeObscuredClient


class ClientObscurerInterface:
    def obscure_client(self, client: ToBeObscuredClient) -> ToBeObscuredClient:
        pass