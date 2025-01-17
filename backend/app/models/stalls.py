from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class StallType(str, enum.Enum):
    FOOD = "food"
    GAME = "game"

class Stall(Base):
    __tablename__ = "stalls"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    type = Column(Enum(StallType))
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    total_revenue = Column(Float, default=0.0)
    pending_payment = Column(Float, default=0.0)
    
    # Relationships
    owner = relationship("User", back_populates="stall")
    menu_items = relationship("MenuItem", back_populates="stall") 