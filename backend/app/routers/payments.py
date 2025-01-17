from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict
import razorpay
from ..database import get_db
from ..models import tickets, users
from ..config import settings
from .auth import get_current_user

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

@router.post("/create-order")
async def create_payment_order(
    amount: int,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    try:
        payment_order = razorpay_client.order.create({
            'amount': amount * 100,  # amount in paisa
            'currency': 'INR',
            'payment_capture': 1
        })
        return payment_order
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/verify")
async def verify_payment(
    payment_details: Dict,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    try:
        # Verify payment signature
        params_dict = {
            'razorpay_payment_id': payment_details['razorpay_payment_id'],
            'razorpay_order_id': payment_details['razorpay_order_id'],
            'razorpay_signature': payment_details['razorpay_signature']
        }
        razorpay_client.utility.verify_payment_signature(params_dict)
        
        # Update ticket payment status
        ticket = db.query(tickets.Ticket).filter(
            tickets.Ticket.id == payment_details['ticket_id']
        ).first()
        
        if ticket:
            ticket.payment_id = payment_details['razorpay_payment_id']
            db.commit()
        
        return {"status": "Payment verified successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment verification failed"
        ) 