#!/usr/bin/env python3
"""
Скрипт для проверки наличия главных изображений ресторанов
"""

import os
import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.restaurant import Restaurant

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_main_images():
    db = SessionLocal()
    try:
        print("\nПроверка главных изображений ресторанов:\n")
        restaurants = db.query(Restaurant).all()
        for r in restaurants:
            print(f"{r.id:2d}. {r.name}")
            print(f"   image_url: {r.image_url}")
            if r.image_url:
                # Убираем ведущий /static для поиска файла
                rel_path = r.image_url[7:] if r.image_url.startswith('/static/') else r.image_url.lstrip('/')
                file_path = os.path.join('static', rel_path)
                if os.path.exists(file_path):
                    print(f"   ✅ Файл найден: {file_path}")
                    print(file_path)
                else:
                    print(f"   ❌ Файл НЕ найден: {file_path}")
                    print(file_path)
            else:
                print("   ❌ image_url не заполнено!")
    finally:
        db.close()

if __name__ == "__main__":
    check_main_images() 