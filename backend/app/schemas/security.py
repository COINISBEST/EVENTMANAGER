from pydantic import BaseModel
from typing import List

class TwoFactorSetup(BaseModel):
    secret_key: str
    backup_codes: List[str]
    qr_code_url: str

class TwoFactorVerify(BaseModel):
    token: str

class TwoFactorBackupCode(BaseModel):
    code: str 