from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReviewBase(BaseModel):
    restaurant_id: int
    rating: float = Field(..., ge=1, le=5, description="Рейтинг от 1 до 5")
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=1, le=5, description="Рейтинг от 1 до 5")
    comment: Optional[str] = None


class ReviewRead(ReviewBase):
    id: int
    user_id: int
    created_at: datetime
    user_name: Optional[str] = None

    class Config:
        orm_mode = True
