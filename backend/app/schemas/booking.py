from pydantic import BaseModel
from enum import Enum
from datetime import date, time
from typing import Optional


class BookingStatus(str, Enum):
    active = "active"
    cancelled = "cancelled"
    completed = "completed"


class BookingBase(BaseModel):
    date: date
    time: time
    guests_count: int
    status: BookingStatus = BookingStatus.active


class BookingCreate(BaseModel):
    table_id: int
    date: date
    time: time
    guests_count: int


class BookingRead(BaseModel):
    id: int
    user_id: int
    table_id: int
    date: date
    time: time
    guests_count: int
    status: BookingStatus
    restaurant_name: Optional[str] = None
    table_seats: Optional[int] = None

    class Config:
        orm_mode = True


class AvailableTable(BaseModel):
    id: int
    seats: int
    is_available: bool


class AvailableTablesResponse(BaseModel):
    restaurant_id: int
    date: date
    time: time
    guests: int
    available_tables: list[AvailableTable]
