from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    cuisine = Column(String, nullable=False)
    price_range = Column(String, nullable=False)
    description = Column(Text)
    rating = Column(Float, default=0.0)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # relationships
    tables = relationship(
        "Table", back_populates="restaurant", cascade="all, delete-orphan")
    reviews = relationship(
        "Review", back_populates="restaurant", cascade="all, delete-orphan")
