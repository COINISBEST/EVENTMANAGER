from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import users, events
from ..schemas import events as event_schemas
from .auth import oauth2_scheme
from ..utils.auth import get_current_user

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@router.post("/", response_model=event_schemas.EventInDB)
async def create_event(
    event: event_schemas.EventCreate,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    if current_user.role != users.UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create events"
        )
    
    db_event = events.Event(**event.dict(), created_by=current_user.id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/", response_model=List[event_schemas.EventInDB])
async def get_events(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return db.query(events.Event).offset(skip).limit(limit).all()

@router.get("/{event_id}", response_model=event_schemas.EventInDB)
async def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    event = db.query(events.Event).filter(events.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event 