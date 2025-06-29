from app.database import SessionLocal
from app.models.restaurant import Restaurant

def debug_restaurants():
    db = SessionLocal()
    try:
        restaurants = db.query(Restaurant).limit(3).all()
        
        for r in restaurants:
            print(f"\nРесторан: {r.name}")
            print(f"gallery type: {type(r.gallery)}")
            print(f"gallery value: {r.gallery}")
            print(f"menu_images type: {type(r.menu_images)}")
            print(f"menu_images value: {r.menu_images}")
            
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_restaurants() 