from app.src.models import Reservation, ToBeObscuredClient, Cliente

class ClientMapper:
    def map_reservation_to_to_be_obscured_client(self, reservation: Reservation) -> ToBeObscuredClient:
        cliente = reservation.cliente
    
        return ToBeObscuredClient(
            first_name=cliente.nome,
            last_name=cliente.cognome,
            email=cliente.email,
            phone=cliente.telefono,
            booking_id=reservation.booking_id,
            is_obscured=True if cliente.nome == "x" * len(cliente.nome) and cliente.cognome == "x" * len(cliente.cognome) else False
        )

    def map_to_be_obscured_client_to_cliente(self, to_be_obscured_client: ToBeObscuredClient) -> Cliente:
        return Cliente(
            nome=to_be_obscured_client.first_name,
            cognome=to_be_obscured_client.last_name,
            email=to_be_obscured_client.email,
            telefono=to_be_obscured_client.phone
        )