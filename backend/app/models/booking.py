from sqlalchemy import Column, Integer, Date, Time, ForeignKey, Enum, String
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class BookingStatus(enum.Enum):
    active = "active"
    cancelled = "cancelled"
    completed = "completed"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    guests_count = Column(Integer, nullable=False)
    status = Column(Enum(BookingStatus),
                    default=BookingStatus.active, nullable=False)
    # relationships
    table = relationship("Table", back_populates="bookings")
