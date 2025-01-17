from pydantic import BaseModel
from datetime import datetime
from ..models.activity import ActivityType

class ActivityOut(BaseModel):
    id: int
    activity_type: ActivityType
    description: str
    ip_address: str | None
    user_agent: str | None
    created_at: datetime

    class Config:
        orm_mode = True 