from pydantic import BaseModel, EmailStr, constr

class PasswordReset(BaseModel):
    token: str
    new_password: constr(min_length=8)

class EmailVerification(BaseModel):
    token: str 