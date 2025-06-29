from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.table import TableCreate, TableRead
from app.models.table import Table
from app.models.restaurant import Restaurant
from app.database import SessionLocal
from app.auth import get_current_admin, get_current_active_user

router = APIRouter(prefix="/tables", tags=["tables"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=TableRead)
def create_table(table: TableCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    # Проверяем, что ресторан существует и принадлежит администратору
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == table.restaurant_id,
        Restaurant.owner_id == admin.id
    ).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found or access denied")
    
    db_table = Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


@router.get("/", response_model=List[TableRead])
def list_tables(db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    if user.role == "admin":
        # Администратор видит все столики своих ресторанов
        restaurants = db.query(Restaurant).filter(Restaurant.owner_id == user.id).all()
        restaurant_ids = [r.id for r in restaurants]
        return db.query(Table).filter(Table.restaurant_id.in_(restaurant_ids)).all()
    else:
        # Обычный пользователь видит только доступные столики
        return db.query(Table).filter(Table.is_available == True).all()


@router.get("/restaurant/{restaurant_id}", response_model=List[TableRead])
def list_restaurant_tables(restaurant_id: int, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    # Проверяем права доступа
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    if user.role != "admin" or restaurant.owner_id != user.id:
        # Обычный пользователь видит только доступные столики
        return db.query(Table).filter(
            Table.restaurant_id == restaurant_id,
            Table.is_available == True
        ).all()
    else:
        # Администратор видит все столики своего ресторана
        return db.query(Table).filter(Table.restaurant_id == restaurant_id).all()


@router.get("/{table_id}", response_model=TableRead)
def get_table(table_id: int, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    # Проверяем права доступа
    restaurant = db.query(Restaurant).filter(Restaurant.id == table.restaurant_id).first()
    if user.role != "admin" or restaurant.owner_id != user.id:
        if not table.is_available:
            raise HTTPException(status_code=403, detail="Access denied")
    
    return table


@router.put("/{table_id}", response_model=TableRead)
def update_table(table_id: int, data: TableCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    # Проверяем, что столик принадлежит ресторану администратора
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == table.restaurant_id,
        Restaurant.owner_id == admin.id
    ).first()
    if not restaurant:
        raise HTTPException(status_code=403, detail="Access denied")
    
    for key, value in data.dict().items():
        setattr(table, key, value)
    db.commit()
    db.refresh(table)
    return table


@router.delete("/{table_id}")
def delete_table(table_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    # Проверяем, что столик принадлежит ресторану администратора
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == table.restaurant_id,
        Restaurant.owner_id == admin.id
    ).first()
    if not restaurant:
        raise HTTPException(status_code=403, detail="Access denied")
    
    db.delete(table)
    db.commit()
    return {"ok": True}


@router.put("/{table_id}/availability")
def toggle_table_availability(table_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    """Переключает доступность столика"""
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    # Проверяем, что столик принадлежит ресторану администратора
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == table.restaurant_id,
        Restaurant.owner_id == admin.id
    ).first()
    if not restaurant:
        raise HTTPException(status_code=403, detail="Access denied")
    
    table.is_available = not table.is_available
    db.commit()
    db.refresh(table)
    return {"ok": True, "is_available": table.is_available}
