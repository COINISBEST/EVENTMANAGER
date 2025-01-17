from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime

class PasswordHistory(Base):
    __tablename__ = "password_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User")

class TwoFactorAuth(Base):
    __tablename__ = "two_factor_auth"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    secret_key = Column(String)
    is_enabled = Column(Boolean, default=False)
    backup_codes = Column(String)  # Stored as JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="two_factor_auth") 

class UserDevice(Base):
    __tablename__ = "user_devices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    device_name = Column(String)  # e.g., "Chrome on Windows"
    device_id = Column(String, unique=True)  # Unique identifier for device
    ip_address = Column(String)
    user_agent = Column(String)
    last_used = Column(DateTime)
    is_trusted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    fingerprint = Column(String)
    location_city = Column(String, nullable=True)
    location_country = Column(String, nullable=True)
    location_region = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    last_ip = Column(String)
    suspicious_activity_count = Column(Integer, default=0)

    # Relationships
    user = relationship("User") 