from pydantic import BaseModel
from typing import Optional
from ..models.tickets import TicketType

class TicketBase(BaseModel):
    event_id: int
    ticket_type: TicketType
    price: float

class TicketCreate(TicketBase):
    user_id: int

class TicketOut(TicketBase):
    id: int
    qr_code: str
    is_used: bool
    payment_id: Optional[str]

    class Config:
        orm_mode = True 