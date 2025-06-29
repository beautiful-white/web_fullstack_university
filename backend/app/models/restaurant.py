from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, JSON, Time
from sqlalchemy.orm import relationship
from app.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)  # Широта
    longitude = Column(Float, nullable=True)  # Долгота
    cuisine = Column(String, nullable=False)
    price_range = Column(String, nullable=False)
    description = Column(Text)
    rating = Column(Float, default=0.0)
    image_url = Column(String)
    gallery = Column(JSON)  # JSON массив строк
    menu_images = Column(JSON)  # JSON массив строк
    opening_time = Column(Time, nullable=False, default="10:00")  # Время открытия
    closing_time = Column(Time, nullable=False, default="22:00")  # Время закрытия
    slot_duration = Column(Integer, default=90)  # Длительность слота в минутах (90 = 1.5 часа)
    phone = Column(String, nullable=True)  # Номер телефона ресторана
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # relationships
    owner = relationship("User", back_populates="restaurants")
    tables = relationship(
        "Table", back_populates="restaurant", cascade="all, delete-orphan")
    reviews = relationship(
        "Review", back_populates="restaurant", cascade="all, delete-orphan")
