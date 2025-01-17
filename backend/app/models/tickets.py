from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class TicketType(str, enum.Enum):
    GENERAL = "general"
    VIP = "vip"
    EARLY_BIRD = "early_bird"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    ticket_type = Column(Enum(TicketType))
    price = Column(Float)
    qr_code = Column(String)
    is_used = Column(Boolean, default=False)
    payment_id = Column(String)

    # Relationships
    event = relationship("Event", back_populates="tickets")
    user = relationship("User", back_populates="tickets") 