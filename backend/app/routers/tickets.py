from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import qrcode
import io
import base64
from ..database import get_db
from ..models import tickets, users, events
from ..schemas import tickets as ticket_schemas
from ..utils.auth import get_current_user

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

def generate_qr_code(ticket_id: int, event_id: int) -> str:
    # Generate QR code with ticket and event info
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"ticket_id:{ticket_id},event_id:{event_id}")
    qr.make(fit=True)
    
    # Create QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 string
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

@router.post("/book", response_model=ticket_schemas.TicketOut)
async def book_ticket(
    ticket_data: ticket_schemas.TicketCreate,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    # Check if event exists and has capacity
    event = db.query(events.Event).filter(events.Event.id == ticket_data.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Count existing tickets
    ticket_count = db.query(tickets.Ticket).filter(
        tickets.Ticket.event_id == ticket_data.event_id
    ).count()
    
    if ticket_count >= event.capacity:
        raise HTTPException(status_code=400, detail="Event is fully booked")
    
    # Create ticket
    db_ticket = tickets.Ticket(
        **ticket_data.dict(),
        user_id=current_user.id
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    
    # Generate QR code
    db_ticket.qr_code = generate_qr_code(db_ticket.id, db_ticket.event_id)
    db.commit()
    
    return db_ticket

@router.get("/my-tickets", response_model=List[ticket_schemas.TicketOut])
async def get_my_tickets(
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    return db.query(tickets.Ticket).filter(tickets.Ticket.user_id == current_user.id).all()

@router.post("/verify-ticket/{ticket_id}")
async def verify_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    # Check if user is volunteer or admin
    if current_user.role not in [users.UserRole.VOLUNTEER, users.UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only volunteers and admins can verify tickets"
        )
    
    ticket = db.query(tickets.Ticket).filter(tickets.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if ticket.is_used:
        raise HTTPException(status_code=400, detail="Ticket has already been used")
    
    ticket.is_used = True
    db.commit()
    
    return {"status": "Ticket verified successfully"} 