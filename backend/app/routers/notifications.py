from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import notifications
from ..schemas import notifications as notification_schemas
from ..utils.auth import get_current_user

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

@router.get("/", response_model=List[notification_schemas.NotificationOut])
async def get_notifications(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    skip: int = 0,
    limit: int = 50
):
    return db.query(notifications.Notification).filter(
        notifications.Notification.user_id == current_user.id
    ).order_by(
        notifications.Notification.created_at.desc()
    ).offset(skip).limit(limit).all()

@router.put("/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    notification = db.query(notifications.Notification).filter(
        notifications.Notification.id == notification_id,
        notifications.Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    db.commit()
    return {"message": "Notification marked as read"}

@router.put("/read-all")
async def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db.query(notifications.Notification).filter(
        notifications.Notification.user_id == current_user.id,
        notifications.Notification.is_read == False
    ).update({"is_read": True})
    
    db.commit()
    return {"message": "All notifications marked as read"} 