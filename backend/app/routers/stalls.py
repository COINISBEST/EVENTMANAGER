from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import users, stalls
from ..schemas import stalls as stall_schemas
from ..utils.auth import get_current_user

router = APIRouter(
    prefix="/stalls",
    tags=["Stalls"]
)

@router.post("/register", response_model=stall_schemas.StallOut)
async def register_stall(
    stall_data: stall_schemas.StallCreate,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    # Check if user already has a stall
    existing_stall = db.query(stalls.Stall).filter(
        stalls.Stall.owner_id == current_user.id
    ).first()
    
    if existing_stall:
        raise HTTPException(
            status_code=400,
            detail="User already has a registered stall"
        )
    
    # Create new stall
    db_stall = stalls.Stall(**stall_data.dict(), owner_id=current_user.id)
    db.add(db_stall)
    db.commit()
    db.refresh(db_stall)
    return db_stall

@router.get("/my-stall", response_model=stall_schemas.StallOut)
async def get_my_stall(
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    stall = db.query(stalls.Stall).filter(
        stalls.Stall.owner_id == current_user.id
    ).first()
    
    if not stall:
        raise HTTPException(status_code=404, detail="No stall found")
    return stall

@router.put("/update-bank-details")
async def update_bank_details(
    bank_details: stall_schemas.BankDetailsUpdate,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    if current_user.role not in [users.UserRole.FOOD_STALL, users.UserRole.GAME_STALL]:
        raise HTTPException(
            status_code=403,
            detail="Only stall owners can update bank details"
        )
    
    current_user.bank_account_number = bank_details.account_number
    current_user.bank_ifsc = bank_details.ifsc_code
    current_user.bank_account_name = bank_details.account_name
    
    db.commit()
    return {"message": "Bank details updated successfully"}

@router.get("/revenue-summary")
async def get_revenue_summary(
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    if current_user.role not in [users.UserRole.FOOD_STALL, users.UserRole.GAME_STALL, users.UserRole.ADMIN]:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized access"
        )
    
    if current_user.role == users.UserRole.ADMIN:
        # Get all stalls revenue for admin
        all_stalls = db.query(stalls.Stall).all()
        return {
            "stalls_revenue": [
                {
                    "stall_id": stall.id,
                    "stall_name": stall.name,
                    "total_revenue": stall.total_revenue,
                    "pending_payment": stall.pending_payment
                }
                for stall in all_stalls
            ]
        }
    else:
        # Get specific stall revenue for stall owner
        stall = db.query(stalls.Stall).filter(
            stalls.Stall.owner_id == current_user.id
        ).first()
        
        if not stall:
            raise HTTPException(status_code=404, detail="No stall found")
            
        return {
            "total_revenue": stall.total_revenue,
            "pending_payment": stall.pending_payment
        } 