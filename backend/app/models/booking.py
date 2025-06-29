from sqlalchemy import Column, Integer, Date, Time, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    guests = Column(Integer, nullable=False)
    status = Column(String, default="active", nullable=False)
    # relationships
    user = relationship("User", back_populates="bookings")
    table = relationship("Table", back_populates="bookings")
