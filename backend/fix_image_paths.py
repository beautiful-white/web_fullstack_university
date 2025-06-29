#!/usr/bin/env python3
"""
Скрипт для исправления путей к изображениям ресторанов
"""

import os
import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.restaurant import Restaurant

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def fix_image_paths():
    """Исправляет пути к изображениям ресторанов"""
    
    db = SessionLocal()
    
    try:
        print("🔧 Исправляем пути к изображениям ресторанов...")
        
        restaurants = db.query(Restaurant).all()
        
        for restaurant in restaurants:
            # Исправляем главное фото
            if restaurant.image_url and not restaurant.image_url.startswith('/static/'):
                old_path = restaurant.image_url
                new_path = '/static' + restaurant.image_url if not restaurant.image_url.startswith('/') else '/static' + restaurant.image_url
                restaurant.image_url = new_path
                print(f"✅ {restaurant.name}: {old_path} → {new_path}")
            
            # Исправляем галерею
            if restaurant.gallery:
                new_gallery = []
                for path in restaurant.gallery:
                    if not path.startswith('/static/'):
                        new_path = '/static' + path if not path.startswith('/') else '/static' + path
                        new_gallery.append(new_path)
                    else:
                        new_gallery.append(path)
                restaurant.gallery = new_gallery
            
            # Исправляем меню
            if restaurant.menu_images:
                new_menu = []
                for path in restaurant.menu_images:
                    if not path.startswith('/static/'):
                        new_path = '/static' + path if not path.startswith('/') else '/static' + path
                        new_menu.append(new_path)
                    else:
                        new_menu.append(path)
                restaurant.menu_images = new_menu
        
        db.commit()
        print(f"\n✅ Пути к изображениям исправлены для {len(restaurants)} ресторанов!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_image_paths() 