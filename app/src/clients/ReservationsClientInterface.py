from typing import List, Optional, Dict, Any
from app.src.models import Reservation, Cliente

class ReservationsClientInterface:
    def get_reservations(self, filters: Optional[Dict[str, Any]] = None) -> List[Reservation]:
        pass

    def get_reservation_by_booking_id(self, booking_id: str) -> Reservation:
        pass

    def update_reservation_client(self, booking_id: str, client: Cliente) -> Reservation:
        pass