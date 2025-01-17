from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, events, tickets, payments, stalls, menu_items, orders, notifications
from .database import engine
from .models import users, events, tickets, stalls
from .middleware.security import SecurityHeadersMiddleware, RequestLoggingMiddleware
from app.core.config import settings

# Create database tables
users.Base.metadata.create_all(bind=engine)
events.Base.metadata.create_all(bind=engine)
tickets.Base.metadata.create_all(bind=engine)
stalls.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Management System")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],  # Replace wildcard with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middleware before CORS
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)

# Include routers
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(tickets.router)
app.include_router(payments.router)
app.include_router(stalls.router)
app.include_router(menu_items.router)
app.include_router(orders.router)
app.include_router(notifications.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Event Management System API"} 