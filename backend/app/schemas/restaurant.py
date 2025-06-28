from pydantic import BaseModel
from typing import Optional


class RestaurantBase(BaseModel):
    name: str
    location: str
    cuisine: str
    price_range: str
    description: Optional[str] = None


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantRead(RestaurantBase):
    id: int
    rating: float
    owner_id: int

    class Config:
        orm_mode = True
