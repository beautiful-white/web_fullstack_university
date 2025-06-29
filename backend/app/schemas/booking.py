from pydantic import BaseModel
from datetime import date, time
from typing import Optional, List


class BookingBase(BaseModel):
    date: date
    time: time
    guests: int


class BookingCreate(BookingBase):
    table_id: int


class BookingRead(BookingBase):
    id: int
    user_id: int
    table_id: int
    status: str
    restaurant_name: Optional[str] = None
    table_seats: Optional[int] = None
    user_email: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True


class AvailableTable(BaseModel):
    id: int
    name: str
    seats: int
    is_available: bool


class AvailableTablesResponse(BaseModel):
    restaurant_id: int
    date: date
    time: time
    guests: int
    available_tables: List[AvailableTable]


class TimeSlot(BaseModel):
    start_time: time
    end_time: time
    is_available: bool


class AvailableTimeSlotsResponse(BaseModel):
    restaurant_id: int
    date: date
    guests: int
    time_slots: List[TimeSlot]
