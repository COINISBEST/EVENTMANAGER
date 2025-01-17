from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from ..models import users, orders, menu_items
from ..schemas import orders as order_schemas
from ..utils.auth import get_current_user
from ..services.notification_service import NotificationService

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("/", response_model=order_schemas.OrderOut)
async def create_order(
    order_data: order_schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    # Calculate total amount and verify items
    total_amount = 0
    order_items = []
    
    for item in order_data.items:
        menu_item = db.query(menu_items.MenuItem).filter(
            menu_items.MenuItem.id == item.menu_item_id,
            menu_items.MenuItem.stall_id == order_data.stall_id,
            menu_items.MenuItem.is_available == True
        ).first()
        
        if not menu_item:
            raise HTTPException(
                status_code=400,
                detail=f"Menu item {item.menu_item_id} not available"
            )
        
        total_amount += menu_item.price * item.quantity
        order_items.append({
            "menu_item_id": menu_item.id,
            "quantity": item.quantity,
            "price_at_time": menu_item.price
        })
    
    # Create order
    db_order = orders.Order(
        user_id=current_user.id,
        stall_id=order_data.stall_id,
        total_amount=total_amount
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Create order items
    for item in order_items:
        db_order_item = orders.OrderItem(
            order_id=db_order.id,
            **item
        )
        db.add(db_order_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/my-orders", response_model=List[order_schemas.OrderOut])
async def get_my_orders(
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    return db.query(orders.Order).filter(
        orders.Order.user_id == current_user.id
    ).order_by(orders.Order.created_at.desc()).all()

@router.put("/{order_id}/status")
async def update_order_status(
    order_id: int,
    status: orders.OrderStatus,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    order = db.query(orders.Order).filter(orders.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Verify permission
    stall = db.query(stalls.Stall).filter(
        stalls.Stall.id == order.stall_id,
        stalls.Stall.owner_id == current_user.id
    ).first()
    
    if not stall:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to update this order"
        )
    
    order.status = status
    if status == orders.OrderStatus.COMPLETED:
        order.completed_at = datetime.utcnow()
    
    # Create notification for order status change
    NotificationService.create_order_status_notification(db, order, status)
    
    db.commit()
    return {"message": "Order status updated successfully"} 