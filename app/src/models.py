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
