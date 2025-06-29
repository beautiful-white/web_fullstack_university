#!/usr/bin/env python3
"""
Скрипт для удаления кавычек из названий ресторанов
"""

import sys
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.restaurant import Restaurant

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def remove_quotes_from_names():
    """Удаляет кавычки из названий ресторанов"""
    
    db = SessionLocal()
    
    try:
        print("🔄 Удаляем кавычки из названий ресторанов...")
        
        restaurants = db.query(Restaurant).all()
        
        for restaurant in restaurants:
            old_name = restaurant.name
            # Убираем одинарные и двойные кавычки
            new_name = old_name.replace("'", "").replace('"', "")
            
            if old_name != new_name:
                restaurant.name = new_name
                print(f"✅ '{old_name}' → '{new_name}'")
        
        db.commit()
        print(f"\n✅ Обновлено {len(restaurants)} ресторанов!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    remove_quotes_from_names() 