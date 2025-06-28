from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey(
        "restaurants.id"), nullable=False)
    seats = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)
    # relationships
    restaurant = relationship("Restaurant", back_populates="tables")
    bookings = relationship(
        "Booking", back_populates="table", cascade="all, delete-orphan")
