from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.database import Base


class UserRole(str, PyEnum):
    guest = "guest"
    user = "user"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    
    # relationships
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    restaurants = relationship("Restaurant", back_populates="owner", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")
