from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from ..config import settings
from pathlib import Path
import jwt
from datetime import datetime, timedelta

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / "../email_templates"
)

class EmailService:
    @staticmethod
    async def send_verification_email(email: str, token: str):
        verify_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
        
        message = MessageSchema(
            subject="Verify your email",
            recipients=[email],
            template_body={
                "verify_url": verify_url
            },
            subtype="html"
        )
        
        fm = FastMail(conf)
        await fm.send_message(message, template_name="verification.html")

    @staticmethod
    async def send_password_reset_email(email: str, token: str):
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        
        message = MessageSchema(
            subject="Reset your password",
            recipients=[email],
            template_body={
                "reset_url": reset_url
            },
            subtype="html"
        )
        
        fm = FastMail(conf)
        await fm.send_message(message, template_name="password_reset.html")

    @staticmethod
    def create_verification_token(email: str) -> str:
        expire = datetime.utcnow() + timedelta(hours=24)
        return jwt.encode(
            {"email": email, "exp": expire, "type": "verification"},
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

    @staticmethod
    def create_password_reset_token(email: str) -> str:
        expire = datetime.utcnow() + timedelta(hours=1)
        return jwt.encode(
            {"email": email, "exp": expire, "type": "password_reset"},
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

    @staticmethod
    async def send_security_alert(
        email: str,
        alert_type: str,
        device_info: dict = None
    ):
        subject_map = {
            "new_device": "New Device Login Detected",
            "password_changed": "Password Changed Successfully",
            "failed_login": "Failed Login Attempt",
            "2fa_enabled": "Two-Factor Authentication Enabled",
            "2fa_disabled": "Two-Factor Authentication Disabled"
        }
        
        message = MessageSchema(
            subject=subject_map.get(alert_type, "Security Alert"),
            recipients=[email],
            template_body={
                "alert_message": alert_type,
                "device_info": device_info
            },
            subtype="html"
        )
        
        fm = FastMail(conf)
        await fm.send_message(message, template_name="security_alert.html") 