from typing import Optional, Dict
import httpx
from fastapi import HTTPException
from app.core.config import settings
import time
from cachetools import TTLCache

class GeolocationService:
    def __init__(self):
        self.cache = TTLCache(maxsize=100, ttl=3600)  # Cache results for 1 hour
        self.rate_limit_tokens = settings.RATE_LIMIT_PER_MINUTE
        self.last_reset = time.time()

    async def get_location_from_ip(self, ip_address: str) -> Optional[Dict]:
        # Check cache first
        if ip_address in self.cache:
            return self.cache[ip_address]

        # Rate limiting
        current_time = time.time()
        if current_time - self.last_reset >= 60:
            self.rate_limit_tokens = settings.RATE_LIMIT_PER_MINUTE
            self.last_reset = current_time

        if self.rate_limit_tokens <= 0:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later."
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"http://ip-api.com/json/{ip_address}")
                response.raise_for_status()
                data = response.json()

                if data.get("status") == "fail":
                    raise HTTPException(
                        status_code=400,
                        detail=f"Failed to get location data: {data.get('message')}"
                    )

                # Cache the result
                self.cache[ip_address] = data
                self.rate_limit_tokens -= 1
                return data

        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Error connecting to geolocation service: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}" 