from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Table, Restaurant

def seed_tables():
    db = SessionLocal()
    try:
        # Получаем все рестораны
        restaurants = db.query(Restaurant).all()
        
        if not restaurants:
            print("Нет ресторанов в базе данных. Сначала создайте рестораны.")
            return
        
        # Добавляем столики для каждого ресторана
        for restaurant in restaurants:
            # Столики на 2 персоны
            for i in range(5):
                table = Table(
                    restaurant_id=restaurant.id,
                    seats=2,
                    is_available=True
                )
                db.add(table)
            
            # Столики на 4 персоны
            for i in range(3):
                table = Table(
                    restaurant_id=restaurant.id,
                    seats=4,
                    is_available=True
                )
                db.add(table)
            
            # Столики на 6 персон
            for i in range(2):
                table = Table(
                    restaurant_id=restaurant.id,
                    seats=6,
                    is_available=True
                )
                db.add(table)
            
            # Столик на 8 персон
            table = Table(
                restaurant_id=restaurant.id,
                seats=8,
                is_available=True
            )
            db.add(table)
        
        db.commit()
        print(f"Добавлено столиков для {len(restaurants)} ресторанов")
        
    except Exception as e:
        print(f"Ошибка при добавлении столиков: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_tables() 