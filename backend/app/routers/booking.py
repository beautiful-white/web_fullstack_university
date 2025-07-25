from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List
from datetime import date, time
from app.schemas.booking import BookingCreate, BookingRead
from app.models.booking import Booking
from app.models.table import Table
from app.models.restaurant import Restaurant
from app.database import SessionLocal
from app.auth import get_current_active_user, get_current_admin

router = APIRouter(prefix="/bookings", tags=["bookings"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_table_availability(db: Session, table_id: int, booking_date: date, booking_time: time, booking_id: int = None):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    if not table.is_available:
        raise HTTPException(status_code=400, detail="Table is not available")
    
    conflicting_booking = db.query(Booking).filter(
        and_(
            Booking.table_id == table_id,
            Booking.date == booking_date,
            Booking.time == booking_time,
            Booking.status == "active",
            Booking.id != booking_id if booking_id else True
        )
    ).first()
    
    if conflicting_booking:
        raise HTTPException(status_code=400, detail="Table is already booked for this date and time")
    
    return table


@router.post("/", response_model=BookingRead)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    check_table_availability(db, booking.table_id, booking.date, booking.time)
    
    table = db.query(Table).filter(Table.id == booking.table_id).first()
    if booking.guests > table.seats:
        raise HTTPException(status_code=400, detail=f"Table can only accommodate {table.seats} guests")
    
    db_booking = Booking(
        user_id=user.id,
        table_id=booking.table_id,
        date=booking.date,
        time=booking.time,
        guests=booking.guests,
        status="active"
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


@router.get("/", response_model=List[BookingRead])
def list_bookings(db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    bookings = db.query(Booking).filter(Booking.user_id == user.id).all()
    
    
    for booking in bookings:
        if booking.table and booking.table.restaurant:
            booking.restaurant_name = booking.table.restaurant.name
            booking.table_seats = booking.table.seats
        if booking.user:
            booking.user_email = booking.user.email
    
    return bookings


@router.get("/all", response_model=List[BookingRead])
def list_all_bookings(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    bookings = db.query(Booking).all()
    
    for booking in bookings:
        if booking.table and booking.table.restaurant:
            booking.restaurant_name = booking.table.restaurant.name
            booking.table_seats = booking.table.seats
        if booking.user:
            booking.user_email = booking.user.email
    
    return bookings


@router.get("/{booking_id}", response_model=BookingRead)
def get_booking(booking_id: int, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    booking = db.query(Booking).filter(
        Booking.id == booking_id, Booking.user_id == user.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Добавляем информацию о ресторане
    if booking.table and booking.table.restaurant:
        booking.restaurant_name = booking.table.restaurant.name
        booking.table_seats = booking.table.seats
    
    return booking


@router.put("/{booking_id}", response_model=BookingRead)
def update_booking(booking_id: int, data: BookingCreate, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    booking = db.query(Booking).filter(
        Booking.id == booking_id, Booking.user_id == user.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if data.date != booking.date or data.time != booking.time or data.table_id != booking.table_id:
        check_table_availability(db, data.table_id, data.date, data.time, booking_id)
    
    table = db.query(Table).filter(Table.id == data.table_id).first()
    if data.guests > table.seats:
        raise HTTPException(status_code=400, detail=f"Table can only accommodate {table.seats} guests")
    
    for key, value in data.dict().items():
        setattr(booking, key, value)
    db.commit()
    db.refresh(booking)
    return booking


@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    booking = db.query(Booking).filter(
        Booking.id == booking_id, Booking.user_id == user.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.status == "active":
        booking.status = "cancelled"
        db.commit()
        return {"message": "Бронирование отменено"}
    else:
        db.delete(booking)
        db.commit()
        return {"message": "Бронирование удалено"}


@router.get("/restaurant/{restaurant_id}/available-tables")
def get_available_tables(restaurant_id: int, date: date, time: time, guests: int, db: Session = Depends(get_db)):
    available_tables = db.query(Table).filter(
        and_(
            Table.restaurant_id == restaurant_id,
            Table.is_available == True,
            Table.seats >= guests
        )
    ).all()
    
    booked_table_ids = db.query(Booking.table_id).filter(
        and_(
            Booking.date == date,
            Booking.time == time,
            Booking.status == "active"
        )
    ).all()
    
    booked_table_ids = [table_id[0] for table_id in booked_table_ids]
    
    free_tables = [table for table in available_tables if table.id not in booked_table_ids]
    
    return {
        "restaurant_id": restaurant_id,
        "date": date,
        "time": time,
        "guests": guests,
        "available_tables": [
            {
                "id": table.id,
                "seats": table.seats,
                "is_available": table.is_available
            } for table in free_tables
        ]
    }
