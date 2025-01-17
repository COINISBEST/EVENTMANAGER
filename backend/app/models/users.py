from sqlalchemy import Column, Integer, String, Enum, Boolean
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    EVENT_TEAM = "event_team"
    VOLUNTEER = "volunteer"
    STUDENT = "student"
    FOOD_STALL = "food_stall"
    GAME_STALL = "game_stall"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    roll_number = Column(String, unique=True, nullable=True)
    full_name = Column(String)
    password = Column(String)
    role = Column(Enum(UserRole))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Bank account details
    bank_account_number = Column(String, nullable=True)
    bank_ifsc = Column(String, nullable=True)
    bank_account_name = Column(String, nullable=True)
    
    # Relationships
    tickets = relationship("Ticket", back_populates="user")
    stall = relationship("Stall", back_populates="owner", uselist=False)
    two_factor_auth = relationship("TwoFactorAuth", back_populates="user", uselist=False) 