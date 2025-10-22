from typing import List

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from typing import List, Optional, Dict, Any

import httpx


from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field
from typing import Optional


class Cliente(BaseModel):
    nome: str = Field(..., description="The name of the client")
    cognome: str = Field(..., description="The surname of the client")
    email: str = Field(..., description="The email of the client")
    telefono: str = Field(..., description="The phone number of the client")

class CheckOutFeedback(BaseModel):
    feedback: str = Field(..., description="The feedback of the check-out")
    privacy: bool = Field(..., description="The privacy of the check-out")
    sentiment: Optional[str] = Field(None, description="The sentiment of the check-out")

class Reservation(BaseModel):
    booking_id: str = Field(..., description="The unique identifier for the reservation")
    alloggio_id: str = Field(..., description="The unique identifier for the alloggio")
    cliente: Cliente = Field(..., description="The client of the reservation")
    check_in: str = Field(..., description="The check-in date of the reservation")
    check_out: Optional[str] = Field(None, description="The check-out date of the reservation")
    ospiti: int = Field(..., description="The number of guests in the reservation")
    stato: str = Field(..., description="The status of the reservation")
    prezzo_totale: float = Field(..., description="The total price of the reservation")
    valuta: str = Field(..., description="The currency of the reservation")
    sorgente: str = Field(..., description="The source of the reservation")
    note: Optional[str] = Field(None, description="The note of the reservation")
    check_out_feedback: Optional[CheckOutFeedback] = Field(..., description="The feedback of the check-out")
    id: str = Field(..., alias="_id", description="The unique identifier for the reservation")
    version: int = Field(..., description="The version of the reservation")
    created_at: str = Field(..., description="The date and time the reservation was created")
    updated_at: str = Field(..., description="The date and time the reservation was updated")

class ToBeObscuredClient(BaseModel):
    first_name: str = Field(..., description="The name of the client")
    last_name: str = Field(..., description="The surname of the client")
    email: str = Field(..., description="The email of the client")
    phone: str = Field(..., description="The phone number of the client")
    booking_id: str = Field(..., description="The booking id of the client")
    is_obscured: bool = Field(..., description="Whether the client data is obscured")

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    reservations_api_base_url: str
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()


class ReservationsClientInterface:
    def get_reservations(self, filters: Optional[Dict[str, Any]] = None) -> List[Reservation]:
        pass

    def get_reservation_by_booking_id(self, booking_id: str) -> Reservation:
        pass

    def update_reservation_client(self, booking_id: str, client: Cliente) -> Reservation:
        pass

class ReservationsClient(ReservationsClientInterface):
    def __init__(self):
        self.base_url = 'http://workshop-test-alb-284392989.eu-west-3.elb.amazonaws.com'

    def get_reservations(self, filters: Optional[Dict[str, Any]] = None) -> List[Reservation]:
        response = httpx.get(f"{self.base_url}/prenotazioni")
        return [Reservation(**reservation) for reservation in response.json()]

    def get_reservation_by_booking_id(self, booking_id: str) -> Reservation:
        response = httpx.get(f"{self.base_url}/prenotazioni/by-booking/{booking_id}")
        return Reservation(**response.json())

    def update_reservation_client(self, booking_id: str, client: Cliente) -> Reservation:
        response = httpx.patch(f"{self.base_url}/prenotazioni/by-booking/{booking_id}/raw", json={
            "cliente": client.model_dump()
        })
        return Reservation(**response.json())

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


class ClientObscurerInterface:
    def obscure_client(self, client: ToBeObscuredClient) -> ToBeObscuredClient:
        pass


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

from typing import List, Optional, Dict, Any
from fastapi import HTTPException

class ClientsService:
    def __init__(self, reservations_client: ReservationsClientInterface, client_mapper: ClientMapper, client_obscurer: ClientObscurerInterface):
        self.reservations_client = reservations_client
        self.client_mapper = client_mapper
        self.client_obscurer = client_obscurer
        
    def get_to_be_obscured_clients(self, filters: Optional[Dict[str, Any]] = None) -> List[ToBeObscuredClient]:
        try:
            reservations = self.reservations_client.get_reservations(filters)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting reservations from remote") from e
            
        # ugly: this logic should be moved in the filter class
        reservations = [reservation for reservation in reservations if reservation.check_out_feedback and not reservation.check_out_feedback.privacy]
        
        #reservations = [reservation for reservation in reservations if reservation.cliente.nome != "x" * len(reservation.cliente.nome) and reservation.cliente.cognome != "x" * len(reservation.cliente.cognome)]
        
        return [self.client_mapper.map_reservation_to_to_be_obscured_client(reservation) for reservation in reservations]


    def obscure_client(self, booking_id: str) -> ToBeObscuredClient:
        try:
            reservation = self.reservations_client.get_reservation_by_booking_id(booking_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting reservation from remote") from e

        client = self.client_mapper.map_reservation_to_to_be_obscured_client(reservation)

        obscured_client = self.client_obscurer.obscure_client(client)

        updated_client = self.client_mapper.map_to_be_obscured_client_to_cliente(obscured_client)

        try:
            updated_client = self.reservations_client.update_reservation_client(booking_id, updated_client)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating reservation in remote") from e

        return obscured_client

def get_reservations_client() -> ReservationsClient:
    return ReservationsClient()

def get_client_mapper() -> ClientMapper:
    return ClientMapper()

def get_client_obscurer() -> ClientObscurer:
    return ClientObscurer()

def get_client_obscurer() -> ClientObscurer:
    return ClientObscurer()

def get_clients_service() -> ClientsService:
    return ClientsService(get_reservations_client(), get_client_mapper(), get_client_obscurer())

app = FastAPI(
    title="Client Obscurer API",
    description="API for managing client data obscuring for privacy compliance",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "alessandra.ricci@wonderfulitaly.eu",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/to-be-obscured-clients", 
         response_model=List[ToBeObscuredClient],
         tags=["clients"],
         summary="Get clients to be obscured",
         description="Retrieve a list of all clients whose data needs to be obscured for privacy compliance.")
def get_clients(clients_service: ClientsService = Depends(get_clients_service)):
    return clients_service.get_to_be_obscured_clients()


@app.post("/api/v1/to-be-obscured-clients/{booking_id}/obscure", 
          response_model=ToBeObscuredClient,
          tags=["clients"],
          summary="Obscure client data",
          description="Obscure the personal data of a specific client identified by booking ID.")
def obscure_client(booking_id: str, clients_service: ClientsService = Depends(get_clients_service)):
    return clients_service.obscure_client(booking_id)

@app.get("/health")
async def health():
    return {
        "status": "ok"
    }
