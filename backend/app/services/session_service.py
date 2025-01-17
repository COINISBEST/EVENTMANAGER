from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..models.users import User
from ..config import settings
import redis
import json

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)

class SessionService:
    @staticmethod
    def create_session(user_id: int, token: str):
        # Store session in Redis with 30 minutes expiry
        session_data = {
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat(),
            'last_activity': datetime.utcnow().isoformat()
        }
        redis_client.setex(
            f"session:{token}",
            settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            json.dumps(session_data)
        )

    @staticmethod
    def get_session(token: str):
        session_data = redis_client.get(f"session:{token}")
        if session_data:
            return json.loads(session_data)
        return None

    @staticmethod
    def update_session(token: str):
        session_data = redis_client.get(f"session:{token}")
        if session_data:
            data = json.loads(session_data)
            data['last_activity'] = datetime.utcnow().isoformat()
            redis_client.setex(
                f"session:{token}",
                settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                json.dumps(data)
            )

    @staticmethod
    def invalidate_session(token: str):
        redis_client.delete(f"session:{token}")

    @staticmethod
    def get_active_sessions(user_id: int):
        sessions = []
        for key in redis_client.scan_iter(f"session:*"):
            session_data = redis_client.get(key)
            if session_data:
                data = json.loads(session_data)
                if data['user_id'] == user_id:
                    sessions.append({
                        'token': key.split(':')[1],
                        **data
                    })
        return sessions 