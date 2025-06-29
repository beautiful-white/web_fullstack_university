#!/usr/bin/env python3
"""
Скрипт для автоматического заполнения image_url для ресторанов, если main.jpg существует
"""

import os
import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.restaurant import Restaurant

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def fix_main_images():
    db = SessionLocal()
    try:
        print("\nАвтоматическое заполнение image_url для ресторанов:\n")
        restaurants = db.query(Restaurant).all()
        for r in restaurants:
            folder = f"static/restaurants/images/restaurant_{r.id}"
            main_path = os.path.join(folder, "main.jpg")
            if os.path.exists(main_path):
                url = f"/static/restaurants/images/restaurant_{r.id}/main.jpg"
                if r.image_url != url:
                    print(f"{r.id:2d}. {r.name}: image_url -> {url}")
                    r.image_url = url
            else:
                print(f"{r.id:2d}. {r.name}: main.jpg не найден")
        db.commit()
        print("\n✅ Готово! Все image_url обновлены, где main.jpg существует.")
    finally:
        db.close()

if __name__ == "__main__":
    fix_main_images() 