from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.table import TableCreate, TableRead
from app.models.table import Table
from app.models.restaurant import Restaurant
from app.database import SessionLocal
from app.auth import get_current_admin

router = APIRouter(prefix="/tables", tags=["tables"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=TableRead)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    db_table = Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


@router.get("/", response_model=List[TableRead])
def list_tables(db: Session = Depends(get_db)):
    return db.query(Table).all()


@router.get("/{table_id}", response_model=TableRead)
def get_table(table_id: int, db: Session = Depends(get_db)):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table


@router.put("/{table_id}", response_model=TableRead)
def update_table(table_id: int, data: TableCreate, db: Session = Depends(get_db)):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    for key, value in data.dict().items():
        setattr(table, key, value)
    db.commit()
    db.refresh(table)
    return table


@router.delete("/{table_id}")
def delete_table(table_id: int, db: Session = Depends(get_db)):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    db.delete(table)
    db.commit()
    return {"ok": True}
