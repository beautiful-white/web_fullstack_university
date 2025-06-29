from app.database import SessionLocal
from app.models.restaurant import Restaurant
from app.models.table import Table
from app.models.booking import Booking

def check_data():
    db = SessionLocal()
    try:
        # Проверяем рестораны
        restaurants = db.query(Restaurant).all()
        print(f"Найдено ресторанов: {len(restaurants)}")
        
        for restaurant in restaurants:
            print(f"\nРесторан: {restaurant.name}")
            print(f"  Время работы: {restaurant.opening_time} - {restaurant.closing_time}")
            print(f"  Длительность слота: {restaurant.slot_duration} минут")
            
            # Проверяем столики
            tables = db.query(Table).filter(Table.restaurant_id == restaurant.id).all()
            print(f"  Столиков: {len(tables)}")
            
            for table in tables:
                print(f"    Столик {table.id}: {table.seats} мест, доступен: {table.is_available}")
            
            # Проверяем брони
            bookings = db.query(Booking).join(Table).filter(Table.restaurant_id == restaurant.id).all()
            print(f"  Бронирований: {len(bookings)}")
            
    finally:
        db.close()

if __name__ == "__main__":
    check_data() 