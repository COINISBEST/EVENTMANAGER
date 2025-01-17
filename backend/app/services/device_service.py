from sqlalchemy.orm import Session
from fastapi import Request
import hashlib
import user_agents
from ..models.security import UserDevice
from datetime import datetime
from .geolocation_service import GeolocationService
from .fingerprint_service import FingerprintService

class DeviceService:
    @staticmethod
    def generate_device_id(request: Request, user_id: int) -> str:
        """Generate a unique device identifier"""
        user_agent = request.headers.get("user-agent", "")
        ip = request.client.host
        unique_string = f"{user_id}:{user_agent}:{ip}"
        return hashlib.sha256(unique_string.encode()).hexdigest()

    @staticmethod
    def get_device_info(request: Request) -> dict:
        """Extract device information from request"""
        user_agent_string = request.headers.get("user-agent", "")
        user_agent = user_agents.parse(user_agent_string)
        ip_address = request.client.host
        
        # Get location info
        location = GeolocationService.get_ip_location(ip_address)
        
        # Get browser fingerprint
        fingerprint = FingerprintService.generate_fingerprint(request)
        
        return {
            "device_name": f"{user_agent.browser.family} on {user_agent.os.family}",
            "user_agent": user_agent_string,
            "ip_address": ip_address,
            "location": location,
            "fingerprint": fingerprint['hash'],
            "timestamp": datetime.utcnow().isoformat()
        }

    @staticmethod
    def register_device(
        db: Session,
        user_id: int,
        request: Request
    ) -> UserDevice:
        device_id = DeviceService.generate_device_id(request, user_id)
        device_info = DeviceService.get_device_info(request)
        
        existing_device = db.query(UserDevice).filter(
            UserDevice.device_id == device_id
        ).first()
        
        if existing_device:
            existing_device.last_used = datetime.utcnow()
            existing_device.ip_address = device_info["ip_address"]
            db.commit()
            return existing_device
        
        new_device = UserDevice(
            user_id=user_id,
            device_id=device_id,
            device_name=device_info["device_name"],
            user_agent=device_info["user_agent"],
            ip_address=device_info["ip_address"],
            last_used=datetime.utcnow()
        )
        
        db.add(new_device)
        db.commit()
        db.refresh(new_device)
        return new_device

    @staticmethod
    def get_user_devices(
        db: Session,
        user_id: int
    ):
        return db.query(UserDevice).filter(
            UserDevice.user_id == user_id
        ).order_by(UserDevice.last_used.desc()).all() 