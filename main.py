from typing import List

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.services import ClientsService
from src.dependencies import get_clients_service
from src.models import ToBeObscuredClient

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