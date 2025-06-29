from pydantic import BaseModel
from typing import Optional, List
from datetime import time


class RestaurantBase(BaseModel):
    name: str
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    cuisine: str
    price_range: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    gallery: Optional[List[str]] = None
    menu_images: Optional[List[str]] = None
    opening_time: time = time(10, 0)  # 10:00 по умолчанию
    closing_time: time = time(22, 0)  # 22:00 по умолчанию
    slot_duration: int = 90  # 90 минут = 1.5 часа


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantRead(RestaurantBase):
    id: int
    rating: float
    owner_id: int

    class Config:
        orm_mode = True
        from_attributes = True
