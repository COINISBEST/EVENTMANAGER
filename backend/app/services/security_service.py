from fastapi import HTTPException, status
import re
from typing import Optional, List
import ipaddress
from ..config import settings
import pyotp
import json
from sqlalchemy.orm import Session
from ..database import PasswordHistory
from fastapi.security import CryptContext

class SecurityService:
    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """
        Validate password strength:
        - At least 8 characters
        - Contains uppercase and lowercase letters
        - Contains numbers
        - Contains special characters
        """
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    @staticmethod
    def check_ip_whitelist(ip: str) -> bool:
        if not settings.IP_WHITELIST:
            return True
        return ip in settings.IP_WHITELIST

    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """Basic input sanitization"""
        if not input_str:
            return input_str
        # Remove potentially dangerous characters
        return re.sub(r'[<>\'";]', '', input_str) 

    @staticmethod
    def generate_totp_secret():
        return pyotp.random_base32()

    @staticmethod
    def generate_backup_codes(count: int = 8) -> List[str]:
        return [secrets.token_hex(4) for _ in range(count)]

    @staticmethod
    def verify_totp(secret: str, token: str) -> bool:
        totp = pyotp.TOTP(secret)
        return totp.verify(token)

    @staticmethod
    def check_password_history(
        db: Session,
        user_id: int,
        new_password: str,
        pwd_context: CryptContext
    ) -> bool:
        """Check if password was used recently"""
        history = db.query(PasswordHistory).filter(
            PasswordHistory.user_id == user_id
        ).order_by(
            PasswordHistory.created_at.desc()
        ).limit(settings.PASSWORD_HISTORY_SIZE).all()

        for old_password in history:
            if pwd_context.verify(new_password, old_password.password_hash):
                return False
        return True

    @staticmethod
    def add_to_password_history(
        db: Session,
        user_id: int,
        password_hash: str
    ):
        # Add new password to history
        history_entry = PasswordHistory(
            user_id=user_id,
            password_hash=password_hash
        )
        db.add(history_entry)

        # Remove old entries if exceeding limit
        old_entries = db.query(PasswordHistory).filter(
            PasswordHistory.user_id == user_id
        ).order_by(
            PasswordHistory.created_at.desc()
        ).offset(settings.PASSWORD_HISTORY_SIZE).all()

        for entry in old_entries:
            db.delete(entry)

        db.commit() 