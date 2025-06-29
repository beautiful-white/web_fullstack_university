from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash

def update_password():
    db = SessionLocal()
    try:
        # Обновляем пароль для пользователя
        email = "aboba69@mail.ru"
        new_password = "123456"
        
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"Пользователь с email {email} не найден")
            return
        
        print(f"Обновляем пароль для пользователя: {user.email}")
        
        # Создаем новый хеш пароля
        new_hash = get_password_hash(new_password)
        user.hashed_password = new_hash
        
        db.commit()
        print(f"Пароль обновлен для пользователя {user.email}")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    update_password() 