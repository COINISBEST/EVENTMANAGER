from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from ..models.users import UserRole

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    roll_number: Optional[str] = None

class UserCreate(UserBase):
    password: constr(min_length=8)
    role: UserRole

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    roll_number: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_ifsc: Optional[str] = None
    bank_account_name: Optional[str] = None

class UserOut(UserBase):
    id: int
    role: UserRole
    is_active: bool
    unread_notifications: int = 0
    bank_account_number: Optional[str] = None
    bank_ifsc: Optional[str] = None
    bank_account_name: Optional[str] = None

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str 