import requests
from typing import Optional, Dict
from ..config import settings

class GeolocationService:
    @staticmethod
    def get_ip_location(ip: str) -> Optional[Dict]:
        """Get location information from IP address using ipapi.co"""
        try:
            response = requests.get(f'https://ipapi.co/{ip}/json/')
            if response.status_code == 200:
                data = response.json()
                return {
                    'city': data.get('city'),
                    'region': data.get('region'),
                    'country': data.get('country_name'),
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude')
                }
        except Exception:
            return None
        return None 