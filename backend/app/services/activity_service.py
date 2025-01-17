from sqlalchemy.orm import Session
from fastapi import Request
from ..models.activity import UserActivity, ActivityType
from datetime import datetime

class ActivityService:
    @staticmethod
    def log_activity(
        db: Session,
        user_id: int,
        activity_type: ActivityType,
        description: str,
        request: Request = None
    ):
        activity = UserActivity(
            user_id=user_id,
            activity_type=activity_type,
            description=description,
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None
        )
        db.add(activity)
        db.commit()
        return activity

    @staticmethod
    def get_user_activities(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 50
    ):
        return db.query(UserActivity).filter(
            UserActivity.user_id == user_id
        ).order_by(
            UserActivity.created_at.desc()
        ).offset(skip).limit(limit).all() 