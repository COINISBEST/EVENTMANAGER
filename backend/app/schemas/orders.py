from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .menu_items import MenuItemOut
from ..models.orders import OrderStatus

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int

class OrderCreate(BaseModel):
    stall_id: int
    items: List[OrderItemCreate]

class OrderItemOut(BaseModel):
    id: int
    menu_item: MenuItemOut
    quantity: int
    price_at_time: float

    class Config:
        orm_mode = True

class OrderOut(BaseModel):
    id: int
    stall_id: int
    total_amount: float
    status: OrderStatus
    created_at: datetime
    completed_at: Optional[datetime]
    items: List[OrderItemOut]

    class Config:
        orm_mode = True 