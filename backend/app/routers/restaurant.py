from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import date, time
from app.schemas.restaurant import RestaurantCreate, RestaurantRead
from app.schemas.booking import AvailableTablesResponse, AvailableTable
from app.models.restaurant import Restaurant
from app.models.table import Table
from app.models.booking import Booking, BookingStatus
from app.database import SessionLocal
from app.auth import get_current_admin, get_current_active_user
import os
import shutil

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

UPLOAD_DIR = os.path.join(os.path.dirname(
    __file__), '../../static/restaurants')
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=RestaurantRead)
def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_restaurant = Restaurant(**restaurant.dict(), owner_id=admin.id)
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


@router.get("/", response_model=List[RestaurantRead])
def list_restaurants(
    db: Session = Depends(get_db),
    location: Optional[str] = Query(None),
    cuisine: Optional[str] = Query(None),
    price_range: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None)
):
    query = db.query(Restaurant)
    if location:
        query = query.filter(Restaurant.location == location)
    if cuisine:
        query = query.filter(Restaurant.cuisine == cuisine)
    if price_range:
        query = query.filter(Restaurant.price_range == price_range)
    if min_rating:
        query = query.filter(Restaurant.rating >= min_rating)
    return query.all()


@router.get("/{restaurant_id}", response_model=RestaurantRead)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.get("/{restaurant_id}/available-tables", response_model=AvailableTablesResponse)
def get_restaurant_available_tables(
    restaurant_id: int, 
    date: date, 
    time: time, 
    guests: int, 
    db: Session = Depends(get_db)
):
    """Получает доступные столики для ресторана на указанную дату и время"""
    # Проверяем, что ресторан существует
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Получаем все столики ресторана с достаточной вместимостью
    available_tables = db.query(Table).filter(
        and_(
            Table.restaurant_id == restaurant_id,
            Table.is_available == True,
            Table.seats >= guests
        )
    ).all()
    
    # Фильтруем столики, которые уже забронированы на это время
    booked_table_ids = db.query(Booking.table_id).filter(
        and_(
            Booking.date == date,
            Booking.time == time,
            Booking.status == BookingStatus.active
        )
    ).all()
    
    booked_table_ids = [table_id[0] for table_id in booked_table_ids]
    
    # Возвращаем только свободные столики
    free_tables = [table for table in available_tables if table.id not in booked_table_ids]
    
    return AvailableTablesResponse(
        restaurant_id=restaurant_id,
        date=date,
        time=time,
        guests=guests,
        available_tables=[
            AvailableTable(
                id=table.id,
                seats=table.seats,
                is_available=table.is_available
            ) for table in free_tables
        ]
    )


@router.put("/{restaurant_id}", response_model=RestaurantRead)
def update_restaurant(restaurant_id: int, data: RestaurantCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    if restaurant.owner_id != admin.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    for key, value in data.dict().items():
        setattr(restaurant, key, value)
    db.commit()
    db.refresh(restaurant)
    return restaurant


@router.delete("/{restaurant_id}")
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    if restaurant.owner_id != admin.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db.delete(restaurant)
    db.commit()
    return {"ok": True}


@router.post("/{restaurant_id}/upload_photo")
def upload_restaurant_photo(restaurant_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    if restaurant.owner_id != admin.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    filename = f"restaurant_{restaurant_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Сохраняем путь к фото (относительно static) в restaurant.photos (или аналогичное поле)
    # предполагается, что поле photos = Column(String)
    restaurant.photos = filename
    db.commit()
    db.refresh(restaurant)
    return {"photo_url": f"/static/restaurants/{filename}"}
