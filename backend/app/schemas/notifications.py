from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.notifications import NotificationType

class NotificationBase(BaseModel):
    type: NotificationType
    title: str
    message: str

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationOut(NotificationBase):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        orm_mode = True 