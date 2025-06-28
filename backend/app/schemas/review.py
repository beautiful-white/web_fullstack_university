from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ReviewBase(BaseModel):
    rating: float
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    user_id: int
    restaurant_id: int


class ReviewRead(ReviewBase):
    id: int
    user_id: int
    restaurant_id: int
    created_at: datetime

    class Config:
        orm_mode = True
