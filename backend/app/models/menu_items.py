from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    stall_id = Column(Integer, ForeignKey("stalls.id"))
    name = Column(String)
    description = Column(String, nullable=True)
    price = Column(Float)
    is_available = Column(Boolean, default=True)
    
    # Relationships
    stall = relationship("Stall", back_populates="menu_items") 