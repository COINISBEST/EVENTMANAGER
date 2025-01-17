from sqlalchemy.orm import Session
from fastapi import Request
from datetime import datetime, timedelta
from typing import List
from ..models.security import UserDevice
from ..models.activity import UserActivity, ActivityType
from .geolocation_service import GeolocationService

class SecurityMonitoring:
    @staticmethod
    def detect_suspicious_activity(
        db: Session,
        user_id: int,
        request: Request,
        device: UserDevice
    ) -> List[str]:
        warnings = []
        
        # Check for rapid location changes
        if device.latitude and device.longitude:
            new_location = GeolocationService.get_ip_location(request.client.host)
            if new_location:
                # Calculate distance between locations
                distance = calculate_distance(
                    device.latitude,
                    device.longitude,
                    new_location['latitude'],
                    new_location['longitude']
                )
                
                # If distance > 500km in less than 1 hour
                if distance > 500 and (datetime.utcnow() - device.last_used) < timedelta(hours=1):
                    warnings.append("Suspicious location change detected")
                    device.suspicious_activity_count += 1
        
        # Check for multiple failed login attempts
        recent_failed_logins = db.query(UserActivity).filter(
            UserActivity.user_id == user_id,
            UserActivity.activity_type == ActivityType.LOGIN,
            UserActivity.description == "Failed login attempt",
            UserActivity.created_at > datetime.utcnow() - timedelta(hours=1)
        ).count()
        
        if recent_failed_logins >= 5:
            warnings.append("Multiple failed login attempts detected")
        
        # Check for unusual time patterns
        hour = datetime.utcnow().hour
        if 0 <= hour <= 4:  # Unusual login hours
            warnings.append("Login attempt during unusual hours")
        
        return warnings

    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in kilometers using Haversine formula"""
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        
        return distance 