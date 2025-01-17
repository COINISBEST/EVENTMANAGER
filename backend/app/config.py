from pydantic import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    RAZORPAY_KEY_ID: str
    RAZORPAY_KEY_SECRET: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    FRONTEND_URL: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    SESSION_EXPIRE_MINUTES: int = 30
    IP_WHITELIST: Optional[List[str]] = None
    MAX_LOGIN_ATTEMPTS: int = 5
    LOGIN_ATTEMPT_WINDOW: int = 300  # 5 minutes
    PASSWORD_HISTORY_SIZE: int = 5

    class Config:
        env_file = ".env"

settings = Settings() 