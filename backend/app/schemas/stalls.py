from pydantic import BaseModel
from typing import Optional
from ..models.stalls import StallType

class StallBase(BaseModel):
    name: str
    description: str
    type: StallType

class StallCreate(StallBase):
    pass

class StallOut(StallBase):
    id: int
    owner_id: int
    is_active: bool
    total_revenue: float
    pending_payment: float

    class Config:
        orm_mode = True

class BankDetailsUpdate(BaseModel):
    account_number: str
    ifsc_code: str
    account_name: str 