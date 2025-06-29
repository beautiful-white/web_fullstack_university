from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import date, time
from app.schemas.restaurant import RestaurantCreate, RestaurantRead
from app.schemas.booking import AvailableTablesResponse, AvailableTable, AvailableTimeSlotsResponse
from app.schemas.review import ReviewRead
from app.models.restaurant import Restaurant
from app.models.table import Table
from app.models.booking import Booking
from app.models.review import Review
from app.database import SessionLocal
from app.auth import get_current_admin, get_current_active_user
from app.utils.time_slots import get_available_time_slots
import os
import shutil
from math import radians, cos, sin, asin, sqrt

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '../../static/restaurants/images')
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
    R = 6371
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
    query = db.query(Restaurant)
    
    if location:
        query = query.filter(Restaurant.location.ilike(f"%{location}%"))
    if cuisine:
        query = query.filter(Restaurant.cuisine == cuisine)
    if price_range:
        query = query.filter(Restaurant.price_range == price_range)
    if min_rating is not None:
        query = query.filter(Restaurant.rating >= min_rating)
    
    restaurants = query.all()
    
    if lat is not None and lon is not None:
        restaurants_with_coords = []
        for r in restaurants:
            if r.latitude is not None and r.longitude is not None:
                distance = haversine(lat, lon, r.latitude, r.longitude)
                if radius is None or distance <= radius:
                    restaurants_with_coords.append((r, distance))
        
        if sort_by == "distance":
            reverse = sort_order == "desc"
            restaurants_with_coords.sort(key=lambda x: x[1], reverse=reverse)
        
        restaurants = [r[0] for r in restaurants_with_coords]
    else:
        if sort_by == "rating":
            reverse = sort_order == "desc"
            restaurants.sort(key=lambda r: r.rating or 0, reverse=reverse)
        elif sort_by == "name":
            reverse = sort_order == "desc"
            restaurants.sort(key=lambda r: r.name.lower(), reverse=reverse)
        else:
            # По умолчанию сортируем по id
            restaurants.sort(key=lambda r: r.id)
    
    return restaurants


@router.get("/nearby", response_model=List[RestaurantRead])
def get_nearby_restaurants(
    lat: float = Query(..., description="Широта пользователя"),
    lon: float = Query(..., description="Долгота пользователя"),
    radius: float = Query(5.0, description="Радиус поиска в км"),
    limit: int = Query(20, description="Максимальное количество результатов"),
    db: Session = Depends(get_db)
):
    restaurants = db.query(Restaurant).all()
    
    nearby_restaurants = []
    for r in restaurants:
        if r.latitude is not None and r.longitude is not None:
            distance = haversine(lat, lon, r.latitude, r.longitude)
            if distance <= radius:
                nearby_restaurants.append((r, distance))
    
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
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
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
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
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
    

    update_data = data.dict()
    for key, value in update_data.items():
        if key == "gallery" and value is None:
            setattr(restaurant, key, [])
        elif key == "menu_images" and value is None:
            setattr(restaurant, key, [])
        else:
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
    
    file_path = os.path.join(UPLOAD_DIR, f"restaurant_{restaurant_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    restaurant.image_url = f"/static/restaurants/restaurant_{restaurant_id}_{file.filename}"
    db.commit()
    
    return {"message": "Photo uploaded successfully", "image_url": restaurant.image_url}


@router.post("/{restaurant_id}/upload_main_image")
def upload_main_image(restaurant_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    """Загрузить главное изображение ресторана"""
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Создаем папку для ресторана если её нет
    restaurant_dir = os.path.join(UPLOAD_DIR, f"restaurant_{restaurant_id}")
    os.makedirs(restaurant_dir, exist_ok=True)
    
    # Сохраняем файл как main.jpg
    file_path = os.path.join(restaurant_dir, "main.jpg")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Обновляем URL в базе данных
    restaurant.image_url = f"/static/restaurants/images/restaurant_{restaurant_id}/main.jpg"
    db.commit()
    
    return {"message": "Main image uploaded successfully", "image_url": restaurant.image_url}


@router.post("/{restaurant_id}/upload_gallery_image")
def upload_gallery_image(restaurant_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    """Загрузить изображение в галерею ресторана"""
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    restaurant_dir = os.path.join(UPLOAD_DIR, f"restaurant_{restaurant_id}")
    os.makedirs(restaurant_dir, exist_ok=True)

    # Находим максимальный номер для галереи
    gallery_files = [f for f in os.listdir(restaurant_dir) if f.startswith("gallery_") and f.endswith(".jpg")]
    max_number = 0
    for fname in gallery_files:
        try:
            num = int(fname.split("_")[1].split(".")[0])
            if num > max_number:
                max_number = num
        except Exception:
            continue
    next_number = max_number + 1

    # Сохраняем файл
    file_path = os.path.join(restaurant_dir, f"gallery_{next_number}.jpg")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Обновляем галерею в базе данных
    current_gallery = restaurant.gallery or []
    new_image_url = f"/static/restaurants/images/restaurant_{restaurant_id}/gallery_{next_number}.jpg"
    current_gallery.append(new_image_url)
    restaurant.gallery = current_gallery
    db.commit()

    return {"message": "Gallery image uploaded successfully", "image_url": new_image_url}


@router.post("/{restaurant_id}/upload_menu_image")
def upload_menu_image(restaurant_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    """Загрузить изображение меню ресторана"""
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")


    restaurant_dir = os.path.join(UPLOAD_DIR, f"restaurant_{restaurant_id}")
    os.makedirs(restaurant_dir, exist_ok=True)

    menu_files = [f for f in os.listdir(restaurant_dir) if f.startswith("menu_") and f.endswith(".jpg")]
    max_number = 0
    for fname in menu_files:
        try:
            num = int(fname.split("_")[1].split(".")[0])
            if num > max_number:
                max_number = num
        except Exception:
            continue
    next_number = max_number + 1

    file_path = os.path.join(restaurant_dir, f"menu_{next_number}.jpg")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    current_menu = restaurant.menu_images or []
    new_image_url = f"/static/restaurants/images/restaurant_{restaurant_id}/menu_{next_number}.jpg"
    current_menu.append(new_image_url)
    restaurant.menu_images = current_menu
    db.commit()

    return {"message": "Menu image uploaded successfully", "image_url": new_image_url}


@router.delete("/{restaurant_id}/delete_image")
def delete_image(restaurant_id: int, image_url: str, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    """Удалить изображение ресторана"""
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Извлекаем имя файла из URL
    file_name = image_url.split('/')[-1]
    file_path = os.path.join(UPLOAD_DIR, f"restaurant_{restaurant_id}", file_name)
    
    # Удаляем файл если он существует
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Обновляем базу данных
    if image_url == restaurant.image_url:
        restaurant.image_url = None
    elif restaurant.gallery and image_url in restaurant.gallery:
        restaurant.gallery.remove(image_url)
    elif restaurant.menu_images and image_url in restaurant.menu_images:
        restaurant.menu_images.remove(image_url)
    
    db.commit()
    
    return {"message": "Image deleted successfully"}


@router.get("/{restaurant_id}/images")
def get_restaurant_images(restaurant_id: int, db: Session = Depends(get_db)):
    """Получить список всех изображений ресторана"""
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    restaurant_dir = os.path.join(UPLOAD_DIR, f"restaurant_{restaurant_id}")
    
    images = {
        "main_image": restaurant.image_url,
        "gallery": restaurant.gallery or [],
        "menu_images": restaurant.menu_images or [],
        "available_files": []
    }
    
    # Получаем список файлов в папке ресторана
    if os.path.exists(restaurant_dir):
        files = os.listdir(restaurant_dir)
        images["available_files"] = [f"/static/restaurants/images/restaurant_{restaurant_id}/{file}" for file in files]
    
    return images


@router.get("/{restaurant_id}/reviews", response_model=List[ReviewRead])
def get_restaurant_reviews(restaurant_id: int, db: Session = Depends(get_db)):
    """Получить отзывы для конкретного ресторана"""
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    reviews = db.query(Review).filter(
        Review.restaurant_id == restaurant_id
    ).order_by(Review.created_at.desc()).all()
    
    for review in reviews:
        if review.user:
            review.user_name = review.user.name
    
    return reviews
