from src.clients.ReservationsClient import ReservationsClient
from src.services.ClientsService import ClientsService
from src.mappers.ClientMapper import ClientMapper
from src.obscurers.ClientObscurer import ClientObscurer

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