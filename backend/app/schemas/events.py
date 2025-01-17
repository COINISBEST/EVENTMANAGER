from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    name: str
    description: str
    venue: str
    date: datetime
    capacity: int
    poster_url: Optional[str] = None

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    is_active: Optional[bool] = None

class EventInDB(EventBase):
    id: int
    is_active: bool
    created_at: datetime
    created_by: int

    class Config:
        orm_mode = True 