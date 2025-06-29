from app.database import engine
from app.models import user, restaurant, table, booking, review
from seed_restaurants import seed_restaurants

def recreate_database():
    try:
        print("Dropping all tables...")
        user.Base.metadata.drop_all(bind=engine)
        print("✓ Tables dropped successfully!")
        
        print("\nCreating database tables...")
        user.Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully!")
        
        print("\nSeeding restaurants...")
        seed_restaurants()
        print("✓ Restaurants seeded successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    recreate_database() 