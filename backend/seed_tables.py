from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Restaurant, Table

def seed_tables():
    db = SessionLocal()
    try:
        # Получаем все рестораны
        restaurants = db.query(Restaurant).all()
        
        for restaurant in restaurants:
            # Проверяем, есть ли уже столики у этого ресторана
            existing_tables = db.query(Table).filter(Table.restaurant_id == restaurant.id).count()
            
            if existing_tables == 0:
                # Добавляем столики разной вместимости
                tables_data = [
                    {"seats": 2, "is_available": True},
                    {"seats": 2, "is_available": True},
                    {"seats": 4, "is_available": True},
                    {"seats": 4, "is_available": True},
                    {"seats": 6, "is_available": True},
                    {"seats": 8, "is_available": True},
                ]
                
                for table_data in tables_data:
                    db_table = Table(
                        restaurant_id=restaurant.id,
                        seats=table_data["seats"],
                        is_available=table_data["is_available"]
                    )
                    db.add(db_table)
                
                print(f"Добавлено {len(tables_data)} столиков для ресторана '{restaurant.name}'")
        
        db.commit()
        print("Столики успешно добавлены!")
        
    except Exception as e:
        print(f"Ошибка при добавлении столиков: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed_tables() 