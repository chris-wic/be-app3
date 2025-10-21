from typing import List, Optional, Dict, Any

import httpx

from src.clients.ReservationsClientInterface import ReservationsClientInterface
from src.models import Reservation, Cliente
from src.settings import settings


class ReservationsClient(ReservationsClientInterface):
    def __init__(self):
        self.base_url = settings.reservations_api_base_url

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