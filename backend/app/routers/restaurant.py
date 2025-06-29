from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import date, time
from app.schemas.restaurant import RestaurantCreate, RestaurantRead
from app.schemas.booking import AvailableTablesResponse, AvailableTable, AvailableTimeSlotsResponse
from app.models.restaurant import Restaurant
from app.models.table import Table
from app.models.booking import Booking, BookingStatus
from app.database import SessionLocal
from app.auth import get_current_admin, get_current_active_user
from app.utils.time_slots import get_available_time_slots
import os
import shutil
from math import radians, cos, sin, asin, sqrt

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


def haversine(lat1, lon1, lat2, lon2):
    """Вычисляет расстояние между двумя точками на сфере (в километрах)"""
    R = 6371  # Радиус Земли в км
    lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c


@router.get("/", response_model=List[RestaurantRead])
def list_restaurants(
    db: Session = Depends(get_db),
    location: Optional[str] = Query(None, description="Фильтр по местоположению"),
    cuisine: Optional[str] = Query(None, description="Фильтр по кухне"),
    price_range: Optional[str] = Query(None, description="Фильтр по ценовому диапазону"),
    min_rating: Optional[float] = Query(None, description="Минимальный рейтинг"),
    lat: Optional[float] = Query(None, description="Широта пользователя"),
    lon: Optional[float] = Query(None, description="Долгота пользователя"),
    radius: Optional[float] = Query(None, description="Радиус поиска в км"),
    sort_by: Optional[str] = Query("distance", description="Сортировка: distance, rating, name"),
    sort_order: Optional[str] = Query("asc", description="Порядок сортировки: asc, desc")
):
    """
    Получить список ресторанов с возможностью фильтрации и сортировки.
    
    - **location**: Фильтр по местоположению (текст)
    - **cuisine**: Фильтр по типу кухни
    - **price_range**: Фильтр по ценовому диапазону
    - **min_rating**: Минимальный рейтинг (0.0 - 5.0)
    - **lat**: Широта пользователя для расчета расстояния
    - **lon**: Долгота пользователя для расчета расстояния
    - **radius**: Радиус поиска в километрах
    - **sort_by**: Поле для сортировки (distance, rating, name)
    - **sort_order**: Порядок сортировки (asc, desc)
    """
    query = db.query(Restaurant)
    
    # Применяем фильтры
    if location:
        query = query.filter(Restaurant.location.ilike(f"%{location}%"))
    if cuisine:
        query = query.filter(Restaurant.cuisine == cuisine)
    if price_range:
        query = query.filter(Restaurant.price_range == price_range)
    if min_rating is not None:
        query = query.filter(Restaurant.rating >= min_rating)
    
    restaurants = query.all()
    
    # Если переданы координаты, добавляем расстояние и фильтруем по радиусу
    if lat is not None and lon is not None:
        # Фильтруем рестораны с координатами
        restaurants_with_coords = []
        for r in restaurants:
            if r.latitude is not None and r.longitude is not None:
                distance = haversine(lat, lon, r.latitude, r.longitude)
                # Если указан радиус, фильтруем по нему
                if radius is None or distance <= radius:
                    restaurants_with_coords.append((r, distance))
        
        # Сортируем по расстоянию
        if sort_by == "distance":
            reverse = sort_order == "desc"
            restaurants_with_coords.sort(key=lambda x: x[1], reverse=reverse)
        
        # Возвращаем только рестораны, убирая расстояние из кортежа
        restaurants = [r[0] for r in restaurants_with_coords]
    else:
        # Если координаты не переданы, применяем другие сортировки
        if sort_by == "rating":
            reverse = sort_order == "desc"
            restaurants.sort(key=lambda r: r.rating or 0, reverse=reverse)
        elif sort_by == "name":
            reverse = sort_order == "desc"
            restaurants.sort(key=lambda r: r.name.lower(), reverse=reverse)
    
    return restaurants


@router.get("/nearby", response_model=List[RestaurantRead])
def get_nearby_restaurants(
    lat: float = Query(..., description="Широта пользователя"),
    lon: float = Query(..., description="Долгота пользователя"),
    radius: float = Query(5.0, description="Радиус поиска в км"),
    limit: int = Query(20, description="Максимальное количество результатов"),
    db: Session = Depends(get_db)
):
    """
    Получить ближайшие рестораны в указанном радиусе.
    
    - **lat**: Широта пользователя
    - **lon**: Долгота пользователя  
    - **radius**: Радиус поиска в километрах
    - **limit**: Максимальное количество результатов
    """
    restaurants = db.query(Restaurant).all()
    
    # Вычисляем расстояние для каждого ресторана с координатами
    nearby_restaurants = []
    for r in restaurants:
        if r.latitude is not None and r.longitude is not None:
            distance = haversine(lat, lon, r.latitude, r.longitude)
            if distance <= radius:
                nearby_restaurants.append((r, distance))
    
    # Сортируем по расстоянию и ограничиваем количество
    nearby_restaurants.sort(key=lambda x: x[1])
    nearby_restaurants = nearby_restaurants[:limit]
    
    return [r[0] for r in nearby_restaurants]


@router.get("/{restaurant_id}", response_model=RestaurantRead)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.get("/{restaurant_id}/available-time-slots", response_model=AvailableTimeSlotsResponse)
def get_restaurant_available_time_slots(
    restaurant_id: int,
    date: date,
    guests: int,
    db: Session = Depends(get_db)
):
    """
    Получает доступные временные слоты для ресторана на указанную дату.
    Слоты генерируются на основе времени работы ресторана и длительности слота.
    """
    # Проверяем, что ресторан существует
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Получаем доступные временные слоты
    time_slots = get_available_time_slots(restaurant, date, guests, db)
    
    return AvailableTimeSlotsResponse(
        restaurant_id=restaurant_id,
        date=date,
        guests=guests,
        time_slots=time_slots
    )


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
                name=f"Столик {table.id}",
                seats=table.seats,
                is_available=True
            ) for table in free_tables
        ]
    )


@router.put("/{restaurant_id}", response_model=RestaurantRead)
def update_restaurant(restaurant_id: int, data: RestaurantCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    for key, value in data.dict().items():
        setattr(restaurant, key, value)
    
    db.commit()
    db.refresh(restaurant)
    return restaurant


@router.delete("/{restaurant_id}")
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    db.delete(restaurant)
    db.commit()
    return {"message": "Restaurant deleted successfully"}


@router.post("/{restaurant_id}/upload_photo")
def upload_restaurant_photo(restaurant_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Сохраняем файл
    file_path = os.path.join(UPLOAD_DIR, f"restaurant_{restaurant_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Обновляем URL изображения в базе
    restaurant.image_url = f"/static/restaurants/restaurant_{restaurant_id}_{file.filename}"
    db.commit()
    
    return {"message": "Photo uploaded successfully", "image_url": restaurant.image_url}
