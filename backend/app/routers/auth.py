from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserRead
from app.models.user import User
from app.database import SessionLocal
from app.auth import get_password_hash, verify_password, create_access_token
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class RegisterResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserRead


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/register", response_model=RegisterResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, name=user.name,
                   hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    print("Сохранение пользователя в базу данных")
    db.refresh(db_user)
    
    # Создаем токен доступа с дополнительной информацией
    access_token = create_access_token(data={
        "sub": str(db_user.id),
        "email": db_user.email,
        "name": db_user.name,
        "role": str(db_user.role)
    })
    
    return RegisterResponse(
        access_token=access_token,
        token_type="bearer",
        user=db_user
    )


@router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    print(f"Попытка входа для email: {login_data.username}")
    
    user = db.query(User).filter(User.email == login_data.username).first()
    if not user:
        print(f"Пользователь с email {login_data.username} не найден")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    
    print(f"Пользователь найден: {user.email}, проверяем пароль")
    
    if not verify_password(login_data.password, user.hashed_password):
        print(f"Неверный пароль для пользователя {user.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    
    print(f"Пароль верный, создаем токен для пользователя {user.email}")
    access_token = create_access_token(data={
        "sub": str(user.id),
        "email": user.email,
        "name": user.name,
        "role": str(user.role)
    })
    return {"access_token": access_token, "token_type": "bearer"}
