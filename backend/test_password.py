from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.auth import verify_password, get_password_hash

def test_password():
    db = SessionLocal()
    try:
        # Проверяем конкретного пользователя
        email = "aboba69@mail.ru"  # Замените на нужный email
        password = "123456"  # Замените на нужный пароль
        
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"Пользователь с email {email} не найден")
            return
        
        print(f"Найден пользователь: {user.email}")
        print(f"Хеш пароля: {user.hashed_password}")
        
        # Проверяем пароль
        is_valid = verify_password(password, user.hashed_password)
        print(f"Пароль '{password}' верный: {is_valid}")
        
        # Создаем новый хеш для сравнения
        new_hash = get_password_hash(password)
        print(f"Новый хеш для пароля '{password}': {new_hash}")
        
        # Проверяем новый хеш
        is_valid_new = verify_password(password, new_hash)
        print(f"Новый хеш верный: {is_valid_new}")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_password() 