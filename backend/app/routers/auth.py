from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import users, notifications
from ..schemas import users as user_schemas
from ..services.user_service import UserService
from jose import JWTError, jwt
from datetime import datetime, timedelta
from ..config import settings
from ..services.email_service import EmailService
from ..schemas.auth import PasswordReset, EmailVerification
from ..dependencies.rate_limiter import email_limiter, auth_limiter
from ..services.session_service import SessionService
from ..utils.logger import logger
from ..services.activity_service import ActivityService
from ..models.activity import ActivityType
from ..schemas.security import TwoFactorSetup, TwoFactorVerify, TwoFactorBackupCode
import qrcode
import io
import base64
import json
import pyotp
from ..services.device_service import DeviceService
from ..models.security import UserDevice
from ..services.security_monitoring import SecurityMonitoring

router = APIRouter(tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=user_schemas.UserOut)
async def register_user(
    user: user_schemas.UserCreate,
    db: Session = Depends(get_db)
):
    db_user = UserService.create_user(db, user)
    
    # Send verification email
    token = EmailService.create_verification_token(user.email)
    await EmailService.send_verification_email(user.email, token)
    
    return db_user

@router.post("/token")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    await auth_limiter.check(request)
    
    try:
        user = UserService.get_user_by_email(db, form_data.username)
        if not user or not UserService.verify_password(form_data.password, user.password):
            logger.warning(
                f"Failed login attempt for email: {form_data.username}",
                extra={'request': request}
            )
            # Log failed login attempt
            if user:
                ActivityService.log_activity(
                    db=db,
                    user_id=user.id,
                    activity_type=ActivityType.LOGIN,
                    description="Failed login attempt",
                    request=request
                )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if email is verified
        UserService.check_verified(user)
        
        # Check 2FA if enabled
        if user.two_factor_auth and user.two_factor_auth.is_enabled:
            if not form_data.scopes or "2fa_token" not in form_data.scopes:
                return {
                    "requires_2fa": True,
                    "temp_token": create_access_token(
                        data={"sub": user.email, "temp": True},
                        expires_delta=timedelta(minutes=5)
                    )
                }
            
            # Verify 2FA token
            if not SecurityService.verify_totp(
                user.two_factor_auth.secret_key,
                form_data.scopes["2fa_token"]
            ):
                raise HTTPException(
                    status_code=401,
                    detail="Invalid 2FA token"
                )
        
        access_token = create_access_token(
            data={"sub": user.email, "role": user.role}
        )
        
        # Create session
        SessionService.create_session(user.id, access_token)
        
        # Log successful login
        ActivityService.log_activity(
            db=db,
            user_id=user.id,
            activity_type=ActivityType.LOGIN,
            description="Successful login",
            request=request
        )
        
        logger.info(
            f"Successful login for user: {user.email}",
            extra={'request': request}
        )
        
        # Register device and check for suspicious activity
        device = DeviceService.register_device(db, user.id, request)
        warnings = SecurityMonitoring.detect_suspicious_activity(db, user.id, request, device)
        
        if warnings:
            # Log warnings
            for warning in warnings:
                logger.warning(
                    f"Security warning for user {user.email}: {warning}",
                    extra={'request': request}
                )
            
            # Send security alert
            await EmailService.send_security_alert(
                user.email,
                "suspicious_activity",
                {
                    **DeviceService.get_device_info(request),
                    "warnings": warnings
                }
            )
            
            # If device is not trusted and has suspicious activity, require 2FA
            if not device.is_trusted and device.suspicious_activity_count > 0:
                return {
                    "requires_2fa": True,
                    "temp_token": create_access_token(
                        data={"sub": user.email, "temp": True},
                        expires_delta=timedelta(minutes=5)
                    )
                }
        
        # Send security alert for new device
        if not device.is_trusted:
            device_info = DeviceService.get_device_info(request)
            await EmailService.send_security_alert(
                user.email,
                "new_device",
                device_info
            )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_schemas.UserOut.from_orm(user)
        }
    except Exception as e:
        logger.error(
            f"Login error: {str(e)}",
            extra={'request': request},
            exc_info=True
        )
        raise

@router.get("/me", response_model=user_schemas.UserOut)
async def get_current_user_info(
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    unread_count = db.query(notifications.Notification).filter(
        notifications.Notification.user_id == current_user.id,
        notifications.Notification.is_read == False
    ).count()
    
    return {
        **current_user.__dict__,
        "unread_notifications": unread_count
    }

@router.put("/me", response_model=user_schemas.UserOut)
async def update_user_info(
    user_update: user_schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    return UserService.update_user(db, current_user, user_update)

@router.get("/users", response_model=List[user_schemas.UserOut])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    if current_user.role != users.UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view all users"
        )
    
    return db.query(users.User).offset(skip).limit(limit).all() 

@router.post("/verify-email")
async def verify_email(
    verification: EmailVerification,
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            verification.token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != "verification":
            raise HTTPException(status_code=400, detail="Invalid token type")
        
        email = payload.get("email")
        user = UserService.get_user_by_email(db, email)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.is_verified = True
        db.commit()
        
        return {"message": "Email verified successfully"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Verification link expired")
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid verification token")

@router.post("/forgot-password")
async def forgot_password(
    request: Request,
    email: EmailStr,
    db: Session = Depends(get_db)
):
    await email_limiter.check(request)
    user = UserService.get_user_by_email(db, email)
    if user:
        token = EmailService.create_password_reset_token(email)
        await EmailService.send_password_reset_email(email, token)
    
    # Always return success to prevent email enumeration
    return {"message": "If the email exists, a password reset link has been sent"}

@router.post("/reset-password")
async def reset_password(
    reset_data: PasswordReset,
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            reset_data.token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != "password_reset":
            raise HTTPException(status_code=400, detail="Invalid token type")
        
        email = payload.get("email")
        user = UserService.get_user_by_email(db, email)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        UserService.update_password(db, user, reset_data.new_password)
        return {"message": "Password updated successfully"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Password reset link expired")
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid reset token") 

@router.post("/logout")
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    token: str = Depends(oauth2_scheme)
):
    SessionService.invalidate_session(token)
    logger.info(
        f"User logged out: {current_user.email}",
        extra={'request': request}
    )
    return {"message": "Successfully logged out"}

@router.get("/sessions")
async def get_sessions(
    current_user: User = Depends(get_current_user)
):
    return SessionService.get_active_sessions(current_user.id)

@router.post("/sessions/{token}/invalidate")
async def invalidate_session(
    token: str,
    current_user: User = Depends(get_current_user)
):
    SessionService.invalidate_session(token)
    return {"message": "Session invalidated"} 

@router.get("/activity-history")
async def get_activity_history(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    return ActivityService.get_user_activities(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    ) 

@router.post("/2fa/setup", response_model=TwoFactorSetup)
async def setup_2fa(
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    if current_user.two_factor_auth and current_user.two_factor_auth.is_enabled:
        raise HTTPException(
            status_code=400,
            detail="2FA is already enabled"
        )

    # Generate secret key and backup codes
    secret = SecurityService.generate_totp_secret()
    backup_codes = SecurityService.generate_backup_codes()

    # Create QR code
    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(
        current_user.email,
        issuer_name="Event Management System"
    )

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(provisioning_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert QR code to base64
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    qr_code_base64 = base64.b64encode(buffered.getvalue()).decode()

    # Store in database
    two_factor = TwoFactorAuth(
        user_id=current_user.id,
        secret_key=secret,
        backup_codes=json.dumps(backup_codes)
    )
    db.add(two_factor)
    db.commit()

    return {
        "secret_key": secret,
        "backup_codes": backup_codes,
        "qr_code_url": f"data:image/png;base64,{qr_code_base64}"
    }

@router.post("/2fa/verify")
async def verify_2fa(
    verification: TwoFactorVerify,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    if not current_user.two_factor_auth:
        raise HTTPException(
            status_code=400,
            detail="2FA is not set up"
        )

    if SecurityService.verify_totp(
        current_user.two_factor_auth.secret_key,
        verification.token
    ):
        current_user.two_factor_auth.is_enabled = True
        db.commit()
        return {"message": "2FA enabled successfully"}

    raise HTTPException(
        status_code=400,
        detail="Invalid verification code"
    )

@router.post("/2fa/disable")
async def disable_2fa(
    verification: TwoFactorVerify,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    if not current_user.two_factor_auth or not current_user.two_factor_auth.is_enabled:
        raise HTTPException(
            status_code=400,
            detail="2FA is not enabled"
        )

    if SecurityService.verify_totp(
        current_user.two_factor_auth.secret_key,
        verification.token
    ):
        db.delete(current_user.two_factor_auth)
        db.commit()
        return {"message": "2FA disabled successfully"}

    raise HTTPException(
        status_code=400,
        detail="Invalid verification code"
    )

@router.post("/2fa/backup")
async def use_backup_code(
    backup: TwoFactorBackupCode,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    if not current_user.two_factor_auth or not current_user.two_factor_auth.is_enabled:
        raise HTTPException(
            status_code=400,
            detail="2FA is not enabled"
        )

    backup_codes = json.loads(current_user.two_factor_auth.backup_codes)
    if backup.code in backup_codes:
        # Remove used backup code
        backup_codes.remove(backup.code)
        current_user.two_factor_auth.backup_codes = json.dumps(backup_codes)
        db.commit()
        return {"message": "Backup code accepted"}

    raise HTTPException(
        status_code=400,
        detail="Invalid backup code"
    ) 

@router.get("/devices")
async def get_devices(
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    return DeviceService.get_user_devices(db, current_user.id)

@router.post("/devices/{device_id}/trust")
async def trust_device(
    device_id: str,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    device = db.query(UserDevice).filter(
        UserDevice.device_id == device_id,
        UserDevice.user_id == current_user.id
    ).first()
    
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    device.is_trusted = True
    db.commit()
    return {"message": "Device marked as trusted"}

@router.delete("/devices/{device_id}")
async def remove_device(
    device_id: str,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    device = db.query(UserDevice).filter(
        UserDevice.device_id == device_id,
        UserDevice.user_id == current_user.id
    ).first()
    
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    db.delete(device)
    db.commit()
    return {"message": "Device removed successfully"} 

@router.get("/security-status")
async def get_security_status(
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    devices = DeviceService.get_user_devices(db, current_user.id)
    recent_activities = ActivityService.get_user_activities(
        db, current_user.id, limit=10
    )
    
    return {
        "devices": len(devices),
        "trusted_devices": sum(1 for d in devices if d.is_trusted),
        "suspicious_devices": sum(1 for d in devices if d.suspicious_activity_count > 0),
        "has_2fa": bool(current_user.two_factor_auth and current_user.two_factor_auth.is_enabled),
        "recent_activities": recent_activities,
        "security_score": calculate_security_score(current_user, devices)
    }

def calculate_security_score(user: users.User, devices: List[UserDevice]) -> int:
    score = 50  # Base score
    
    # Add points for security features
    if user.two_factor_auth and user.two_factor_auth.is_enabled:
        score += 20
    
    if any(d.is_trusted for d in devices):
        score += 10
    
    if len(devices) < 5:  # Fewer devices = better security
        score += 10
    
    if not any(d.suspicious_activity_count > 0 for d in devices):
        score += 10
    
    return min(score, 100)  # Cap at 100 