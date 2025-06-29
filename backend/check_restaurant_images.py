#!/usr/bin/env python3
"""
Скрипт для проверки путей к изображениям ресторанов
"""

import os
import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.restaurant import Restaurant

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_restaurant_images():
    """Проверяет пути к изображениям ресторанов"""
    
    db = SessionLocal()
    
    try:
        print("🔍 Проверяем пути к изображениям ресторанов...")
        
        restaurants = db.query(Restaurant).all()
        
        for restaurant in restaurants:
            print(f"\n📋 {restaurant.name} (ID: {restaurant.id}):")
            print(f"   Главное фото: {restaurant.image_url}")
            print(f"   Галерея: {restaurant.gallery}")
            print(f"   Меню: {restaurant.menu_images}")
            
            # Проверяем существование файлов
            if restaurant.image_url:
                file_path = f"static{restaurant.image_url}"
                if os.path.exists(file_path):
                    print(f"   ✅ Главное фото существует: {file_path}")
                else:
                    print(f"   ❌ Главное фото НЕ существует: {file_path}")
            
            if restaurant.gallery:
                for i, gallery_path in enumerate(restaurant.gallery):
                    file_path = f"static{gallery_path}"
                    if os.path.exists(file_path):
                        print(f"   ✅ Галерея {i+1} существует: {file_path}")
                    else:
                        print(f"   ❌ Галерея {i+1} НЕ существует: {file_path}")
            
            if restaurant.menu_images:
                for i, menu_path in enumerate(restaurant.menu_images):
                    file_path = f"static{menu_path}"
                    if os.path.exists(file_path):
                        print(f"   ✅ Меню {i+1} существует: {file_path}")
                    else:
                        print(f"   ❌ Меню {i+1} НЕ существует: {file_path}")
        
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_restaurant_images() 