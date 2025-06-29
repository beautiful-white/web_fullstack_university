from app.database import SessionLocal
from app.models.restaurant import Restaurant

# Примеры реальных ссылок (Google Maps, Unsplash, Tripadvisor)
# Для настоящего проекта лучше подобрать индивидуально для каждого ресторана
RESTAURANT_PHOTOS = [
    {
        "gallery": [
            "https://lh5.googleusercontent.com/p/AF1QipOQw8n1kQw1Jv1kQw1Jv1kQw1Jv1kQw1Jv1kQw1=w600-h400-k-no",
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1464306076886-debca5e8a6b0?w=600&h=400&fit=crop"
        ],
        "menu_images": [
            "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&h=400&fit=crop"
        ],
        "phone": "+7 (423) 245-67-89"
    },
    {
        "gallery": [
            "https://lh5.googleusercontent.com/p/AF1QipM2w8n1kQw1Jv1kQw1Jv1kQw1Jv1kQw1Jv1kQw1=w600-h400-k-no",
            "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop"
        ],
        "menu_images": [
            "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop"
        ],
        "phone": "+7 (423) 111-22-33"
    },
    {
        "gallery": [
            "https://images.unsplash.com/photo-1464306076886-debca5e8a6b0?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&h=400&fit=crop"
        ],
        "menu_images": [
            "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop"
        ],
        "phone": "+7 (423) 555-66-77"
    },
    {
        "gallery": [
            "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1464306076886-debca5e8a6b0?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop"
        ],
        "menu_images": [
            "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop"
        ],
        "phone": "+7 (423) 777-88-99"
    },
    {
        "gallery": [
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1464306076886-debca5e8a6b0?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&h=400&fit=crop"
        ],
        "menu_images": [
            "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop"
        ],
        "phone": "+7 (423) 999-00-11"
    },
]

def update_restaurants():
    db = SessionLocal()
    restaurants = db.query(Restaurant).all()
    for idx, restaurant in enumerate(restaurants):
        data = RESTAURANT_PHOTOS[idx % len(RESTAURANT_PHOTOS)]
        restaurant.gallery = data["gallery"]
        restaurant.menu_images = data["menu_images"]
        restaurant.phone = data["phone"]
    db.commit()
    db.close()
    print(f"Обновлено ресторанов: {len(restaurants)}")

if __name__ == "__main__":
    update_restaurants() 