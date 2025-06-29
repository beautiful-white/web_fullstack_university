from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash

def test_auth():
    db = SessionLocal()
    try:
        # Проверяем, есть ли пользователи в базе
        users = db.query(User).all()
        print(f"Найдено пользователей: {len(users)}")
        
        for user in users:
            print(f"Пользователь: {user.email}, роль: {user.role}")
        
        # Создаем тестового пользователя, если его нет
        test_user = db.query(User).filter(User.email == "test@example.com").first()
        if not test_user:
            test_user = User(
                email="test@example.com",
                hashed_password=get_password_hash("test123"),
                name="Тестовый пользователь",
                role="user"
            )
            db.add(test_user)
            db.commit()
            print("Создан тестовый пользователь: test@example.com / test123")
        else:
            print("Тестовый пользователь уже существует")
            
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_auth() 