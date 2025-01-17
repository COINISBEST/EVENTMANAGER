from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import users, stalls, menu_items
from ..schemas import menu_items as menu_schemas
from ..utils.auth import get_current_user

router = APIRouter(
    prefix="/menu-items",
    tags=["Menu Items"]
)

@router.post("/", response_model=menu_schemas.MenuItemOut)
async def create_menu_item(
    item: menu_schemas.MenuItemCreate,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    # Verify stall ownership
    stall = db.query(stalls.Stall).filter(
        stalls.Stall.id == item.stall_id,
        stalls.Stall.owner_id == current_user.id
    ).first()
    
    if not stall:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to add items to this stall"
        )
    
    db_item = menu_items.MenuItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/stall/{stall_id}", response_model=List[menu_schemas.MenuItemOut])
async def get_stall_menu(stall_id: int, db: Session = Depends(get_db)):
    return db.query(menu_items.MenuItem).filter(
        menu_items.MenuItem.stall_id == stall_id,
        menu_items.MenuItem.is_available == True
    ).all()

@router.put("/{item_id}", response_model=menu_schemas.MenuItemOut)
async def update_menu_item(
    item_id: int,
    item_update: menu_schemas.MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    db_item = db.query(menu_items.MenuItem).join(stalls.Stall).filter(
        menu_items.MenuItem.id == item_id,
        stalls.Stall.owner_id == current_user.id
    ).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for key, value in item_update.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item 