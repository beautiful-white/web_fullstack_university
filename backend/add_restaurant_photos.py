#!/usr/bin/env python3
"""
Скрипт для добавления реальных фотографий ресторанов
"""

import os
import sys
import requests
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.restaurant import Restaurant

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def download_image(url, filepath):
    """Загружает изображение по URL"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Ошибка загрузки {url}: {e}")
        return False

def add_restaurant_photos():
    """Добавляет фотографии для всех ресторанов"""
    
    db = SessionLocal()
    
    # Фотографии для каждого ресторана
    restaurant_photos = {
        1: {  # Ресторан 'Золотой Рог'
            "main": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&h=600&fit=crop",
            "gallery": [
                "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop"
            ],
            "menu": [
                "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=800&h=600&fit=crop"
            ]
        },
        2: {  # Суши-бар 'Сакура'
            "main": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800&h=600&fit=crop",
            "gallery": [
                "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1553621042-f6e147245754?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800&h=600&fit=crop"
            ],
            "menu": [
                "https://images.unsplash.com/photo-1553621042-f6e147245754?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800&h=600&fit=crop"
            ]
        },
        3: {  # Пиццерия 'Марина'
            "main": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800&h=600&fit=crop",
            "gallery": [
                "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800&h=600&fit=crop"
            ],
            "menu": [
                "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800&h=600&fit=crop"
            ]
        },
        4: {  # Ресторан 'Морской'
            "main": "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=600&fit=crop",
            "gallery": [
                "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop"
            ],
            "menu": [
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=600&fit=crop"
            ]
        },
        5: {  # Кафе 'У Моря'
            "main": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop",
            "gallery": [
                "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=600&fit=crop"
            ],
            "menu": [
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop"
            ]
        },
        6: {  # Ресторан 'Восток'
            "main": "https://images.unsplash.com/photo-1553621042-f6e147245754?w=800&h=600&fit=crop",
            "gallery": [
                "https://images.unsplash.com/photo-1553621042-f6e147245754?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1553621042-f6e147245754?w=800&h=600&fit=crop"
            ],
            "menu": [
                "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1553621042-f6e147245754?w=800&h=600&fit=crop"
            ]
        },
        7: {  # Стейк-хаус 'Премиум'
            "main": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800&h=600&fit=crop",
            "gallery": [
                "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop"
            ],
            "menu": [
                "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800&h=600&fit=crop"
            ]
        },
        8: {  # Ресторан 'Панорама'
            "main": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop",
            "gallery": [
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=600&fit=crop"
            ],
            "menu": [
                "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop"
            ]
        },
        9: {  # Ресторан 'Портмейн'
            "main": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop",
            "gallery": [
                "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=600&fit=crop"
            ],
            "menu": [
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop"
            ]
        },
        10: {  # Ресторан 'Океан'
            "main": "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=600&fit=crop",
            "gallery": [
                "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop"
            ],
            "menu": [
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=600&fit=crop"
            ]
        },
        11: {  # Пиццерия 'Домино'
            "main": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800&h=600&fit=crop",
            "gallery": [
                "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800&h=600&fit=crop"
            ],
            "menu": [
                "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800&h=600&fit=crop"
            ]
        },
        12: {  # Ресторан 'Азия'
            "main": "https://images.unsplash.com/photo-1553621042-f6e147245754?w=800&h=600&fit=crop",
            "gallery": [
                "https://images.unsplash.com/photo-1553621042-f6e147245754?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1553621042-f6e147245754?w=800&h=600&fit=crop"
            ],
            "menu": [
                "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1553621042-f6e147245754?w=800&h=600&fit=crop"
            ]
        },
        13: {  # Ресторан 'Модерн'
            "main": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop",
            "gallery": [
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=600&fit=crop"
            ],
            "menu": [
                "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop"
            ]
        },
        14: {  # Ресторан 'Гранд'
            "main": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop",
            "gallery": [
                "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=600&fit=crop"
            ],
            "menu": [
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop"
            ]
        },
        15: {  # Суши-бар 'Токио'
            "main": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800&h=600&fit=crop",
            "gallery": [
                "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1553621042-f6e147245754?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800&h=600&fit=crop"
            ],
            "menu": [
                "https://images.unsplash.com/photo-1553621042-f6e147245754?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800&h=600&fit=crop"
            ]
        },
        16: {  # Ресторан 'Порт'
            "main": "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=600&fit=crop",
            "gallery": [
                "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop"
            ],
            "menu": [
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=600&fit=crop"
            ]
        },
        17: {  # Ресторан 'Классик'
            "main": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop",
            "gallery": [
                "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=600&fit=crop"
            ],
            "menu": [
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=600&fit=crop"
            ]
        }
    }
    
    try:
        print("🔄 Загружаем фотографии для ресторанов...")
        
        for restaurant_id, photos in restaurant_photos.items():
            restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
            if not restaurant:
                print(f"Ресторан с ID {restaurant_id} не найден")
                continue
                
            folder_path = f"static/restaurants/images/restaurant_{restaurant_id}"
            os.makedirs(folder_path, exist_ok=True)
            
            # Загружаем главное фото
            main_path = f"{folder_path}/main.jpg"
            if download_image(photos["main"], main_path):
                restaurant.image_url = f"/static/restaurants/images/restaurant_{restaurant_id}/main.jpg"
                print(f"✅ Главное фото для '{restaurant.name}' загружено")
            
            # Загружаем галерею
            gallery_paths = []
            for i, gallery_url in enumerate(photos["gallery"], 1):
                gallery_path = f"{folder_path}/gallery_{i}.jpg"
                if download_image(gallery_url, gallery_path):
                    gallery_paths.append(f"/static/restaurants/images/restaurant_{restaurant_id}/gallery_{i}.jpg")
            restaurant.gallery = gallery_paths
            print(f"✅ Галерея для '{restaurant.name}' загружена ({len(gallery_paths)} фото)")
            
            # Загружаем меню
            menu_paths = []
            for i, menu_url in enumerate(photos["menu"], 1):
                menu_path = f"{folder_path}/menu_{i}.jpg"
                if download_image(menu_url, menu_path):
                    menu_paths.append(f"/static/restaurants/images/restaurant_{restaurant_id}/menu_{i}.jpg")
            restaurant.menu_images = menu_paths
            print(f"✅ Меню для '{restaurant.name}' загружено ({len(menu_paths)} фото)")
        
        db.commit()
        print("\n✅ Все фотографии успешно загружены и обновлены в базе данных!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_restaurant_photos() 