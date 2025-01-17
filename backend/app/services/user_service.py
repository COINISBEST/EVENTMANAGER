from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from ..models.users import User, UserRole
from ..schemas import users as user_schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    @staticmethod
    def create_user(db: Session, user: user_schemas.UserCreate):
        # Check if email already registered
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if roll number is unique for students
        if user.roll_number and db.query(User).filter(
            User.roll_number == user.roll_number
        ).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Roll number already registered"
            )
        
        # Hash the password
        hashed_password = pwd_context.hash(user.password)
        
        # Create user object
        db_user = User(
            **user.dict(exclude={'password'}),
            password=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(
        db: Session,
        user: User,
        user_update: user_schemas.UserUpdate
    ):
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(user, key, value)
        
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first() 

    @staticmethod
    def update_password(db: Session, user: User, new_password: str):
        hashed_password = pwd_context.hash(new_password)
        user.password = hashed_password
        db.commit()
        return user

    @staticmethod
    def check_verified(user: User):
        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email not verified. Please verify your email first."
            ) 