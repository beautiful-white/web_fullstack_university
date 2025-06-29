from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.schemas.review import ReviewCreate, ReviewRead, ReviewUpdate
from app.models.review import Review
from app.models.restaurant import Restaurant
from app.database import SessionLocal
from app.auth import get_current_active_user

router = APIRouter(prefix="/reviews", tags=["reviews"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def update_restaurant_rating(db: Session, restaurant_id: int):
    avg_rating = db.query(func.avg(Review.rating)).filter(
        Review.restaurant_id == restaurant_id
    ).scalar()
    
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if restaurant:
        restaurant.rating = round(avg_rating, 1) if avg_rating else 0.0
        db.commit()


@router.post("/", response_model=ReviewRead)
def create_review(review: ReviewCreate, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    exists = db.query(Review).filter(
        Review.user_id == user.id,
        Review.restaurant_id == review.restaurant_id
    ).first()
    
    if exists:
        raise HTTPException(
            status_code=400, detail="Вы уже оставляли отзыв для этого ресторана"
        )
    
    if review.rating < 1 or review.rating > 5:
        raise HTTPException(
            status_code=400, detail="Рейтинг должен быть от 1 до 5"
        )
    
    db_review = Review(
        user_id=user.id,
        restaurant_id=review.restaurant_id,
        rating=review.rating,
        comment=review.comment
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    
    update_restaurant_rating(db, review.restaurant_id)
    
    db_review.user_name = user.name
    
    return db_review


@router.get("/restaurant/{restaurant_id}", response_model=List[ReviewRead])
def get_reviews_for_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(
        Review.restaurant_id == restaurant_id
    ).order_by(Review.created_at.desc()).all()
    
    for review in reviews:
        if review.user:
            review.user_name = review.user.name
    
    return reviews


@router.put("/{review_id}", response_model=ReviewRead)
def update_review(
    review_id: int, 
    review_update: ReviewUpdate, 
    db: Session = Depends(get_db), 
    user=Depends(get_current_active_user)
):
    db_review = db.query(Review).filter(
        Review.id == review_id,
        Review.user_id == user.id
    ).first()
    
    if not db_review:
        raise HTTPException(status_code=404, detail="Отзыв не найден")
    
    if review_update.rating and (review_update.rating < 1 or review_update.rating > 5):
        raise HTTPException(
            status_code=400, detail="Рейтинг должен быть от 1 до 5"
        )
    
    if review_update.rating is not None:
        db_review.rating = review_update.rating
    if review_update.comment is not None:
        db_review.comment = review_update.comment
    
    db.commit()
    db.refresh(db_review)
    
    update_restaurant_rating(db, db_review.restaurant_id)
    
    db_review.user_name = user.name
    
    return db_review


@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    db_review = db.query(Review).filter(
        Review.id == review_id,
        Review.user_id == user.id
    ).first()
    
    if not db_review:
        raise HTTPException(status_code=404, detail="Отзыв не найден")
    
    restaurant_id = db_review.restaurant_id
    db.delete(db_review)
    db.commit()
    
    update_restaurant_rating(db, restaurant_id)
    
    return {"message": "Отзыв успешно удален"}


@router.get("/user/", response_model=List[ReviewRead])
def get_user_reviews(db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    reviews = db.query(Review).filter(
        Review.user_id == user.id
    ).order_by(Review.created_at.desc()).all()
    
    for review in reviews:
        review.user_name = user.name
    
    return reviews
