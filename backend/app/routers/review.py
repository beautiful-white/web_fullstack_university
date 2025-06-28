from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.review import ReviewCreate, ReviewRead
from app.models.review import Review
from app.database import SessionLocal
from app.auth import get_current_active_user

router = APIRouter(prefix="/reviews", tags=["reviews"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ReviewRead)
def create_review(review: ReviewCreate, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    exists = db.query(Review).filter(Review.user_id == user.id,
                                     Review.restaurant_id == review.restaurant_id).first()
    if exists:
        raise HTTPException(
            status_code=400, detail="You have already reviewed this restaurant")
    db_review = Review(**review.dict(), user_id=user.id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.get("/restaurant/{restaurant_id}", response_model=List[ReviewRead])
def get_reviews_for_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.restaurant_id == restaurant_id).all()
