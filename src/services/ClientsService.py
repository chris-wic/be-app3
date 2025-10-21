from typing import List, Optional, Dict, Any
from src.mappers.ClientMapper import ClientMapper
from src.clients.ReservationsClientInterface import ReservationsClientInterface
from src.models import ToBeObscuredClient
from src.obscurers.ClientObscurerInterface import ClientObscurerInterface
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