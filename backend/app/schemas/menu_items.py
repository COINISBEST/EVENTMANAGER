from pydantic import BaseModel
from typing import Optional

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

class MenuItemCreate(MenuItemBase):
    stall_id: int

class MenuItemUpdate(MenuItemBase):
    pass

class MenuItemOut(MenuItemBase):
    id: int
    stall_id: int

    class Config:
        orm_mode = True 