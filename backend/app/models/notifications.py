from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime
import enum

class NotificationType(str, enum.Enum):
    ORDER_STATUS = "order_status"
    PAYMENT = "payment"
    EVENT_UPDATE = "event_update"
    SYSTEM = "system"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(Enum(NotificationType))
    title = Column(String)
    message = Column(String)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User") 