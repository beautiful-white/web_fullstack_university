from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Restaurant, User
from app.auth import get_password_hash
from datetime import time

def seed_restaurants():
    db = SessionLocal()
    try:
        # Создаем админа если его нет
        admin = db.query(User).filter(User.email == "admin@restaurant.com").first()
        if not admin:
            admin = User(
                email="admin@restaurant.com",
                hashed_password=get_password_hash("admin123"),
                name="Администратор",
                role="admin"
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("Создан администратор: admin@restaurant.com / admin123")

        # Данные ресторанов Владивостока с координатами
        restaurants_data = [
            {
                "name": "Марио",
                "location": "Владивосток, ул. Светланская, 20",
                "latitude": 43.1198,
                "longitude": 131.8869,
                "cuisine": "Итальянская",
                "price_range": "Средний",
                "description": "Аутентичный итальянский ресторан с пастой, пиццей и морепродуктами. Уютная атмосфера и вид на бухту Золотой Рог. Специализируется на блюдах из свежих морепродуктов в итальянском стиле. Идеальное место для романтического ужина или семейного обеда.",
                "rating": 4.5,
                "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&h=400&fit=crop",
                "opening_time": time(10, 0),  # 10:00
                "closing_time": time(22, 0),  # 22:00
                "slot_duration": 90,  # 1.5 часа
                "gallery": [
                    "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1464306076886-debca5e8a6b0?w=600&h=400&fit=crop"
                ],
                "menu_images": [
                    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop"
                ]
            },
            {
                "name": "Золотой Рог",
                "location": "Владивосток, ул. Адмирала Фокина, 1",
                "latitude": 43.1156,
                "longitude": 131.8854,
                "cuisine": "Русская",
                "price_range": "Высокий",
                "description": "Элитный ресторан с традиционной русской кухней и морепродуктами. Панорамный вид на бухту и мост. Предлагает блюда из свежей рыбы, крабов, устриц и традиционные русские блюда. Изысканный интерьер и профессиональное обслуживание.",
                "rating": 4.7,
                "image_url": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&h=400&fit=crop",
                "opening_time": time(11, 0),  # 11:00
                "closing_time": time(23, 0),  # 23:00
                "slot_duration": 120,  # 2 часа
                "gallery": [
                    "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=600&h=400&fit=crop"
                ],
                "menu_images": [
                    "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=600&h=400&fit=crop"
                ]
            },
            {
                "name": "Токио",
                "location": "Владивосток, ул. Алеутская, 15",
                "latitude": 43.1223,
                "longitude": 131.8891,
                "cuisine": "Японская",
                "price_range": "Средний",
                "description": "Ресторан японской кухни с суши, роллами и терияки. Свежие морепродукты и традиционные блюда. Мастер-сушисты готовят блюда прямо перед гостями. Аутентичная атмосфера и качественные ингредиенты.",
                "rating": 4.3,
                "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=600&h=400&fit=crop",
                "opening_time": time(12, 0),  # 12:00
                "closing_time": time(21, 0),  # 21:00
                "slot_duration": 90,  # 1.5 часа
                "gallery": [
                    "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop"
                ],
                "menu_images": [
                    "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop"
                ]
            },
            {
                "name": "Порт",
                "location": "Владивосток, ул. Набережная, 5",
                "latitude": 43.1189,
                "longitude": 131.8834,
                "cuisine": "Морепродукты",
                "price_range": "Высокий",
                "description": "Ресторан морепродуктов с видом на порт. Свежие крабы, креветки, устрицы и рыба. Прямые поставки с рыболовецких судов. Элегантный интерьер в морском стиле и панорамные окна.",
                "rating": 4.6,
                "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=600&h=400&fit=crop",
                "opening_time": time(10, 0),  # 10:00
                "closing_time": time(22, 0),  # 22:00
                "slot_duration": 90,  # 1.5 часа
                "gallery": [
                    "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop"
                ],
                "menu_images": [
                    "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop"
                ]
            },
            {
                "name": "Китайский Двор",
                "location": "Владивосток, ул. Семеновская, 12",
                "latitude": 43.1212,
                "longitude": 131.8876,
                "cuisine": "Китайская",
                "price_range": "Средний",
                "description": "Аутентичный китайский ресторан с уткой по-пекински, димсамами и традиционными блюдами. Интерьер в стиле древнего Китая. Специализируется на кантонской и сычуаньской кухне.",
                "rating": 4.2,
                "image_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&h=400&fit=crop",
                "opening_time": time(11, 0),  # 11:00
                "closing_time": time(21, 30),  # 21:30
                "slot_duration": 90,  # 1.5 часа
                "gallery": [
                    "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop"
                ],
                "menu_images": [
                    "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop"
                ]
            },
            {
                "name": "Гриль Хаус",
                "location": "Владивосток, ул. Фокина, 8",
                "latitude": 43.1167,
                "longitude": 131.8845,
                "cuisine": "Европейская",
                "price_range": "Средний",
                "description": "Ресторан европейской кухни с грилем, стейками и пастой. Современный интерьер и уютная атмосфера. Специализируется на мясных блюдах, приготовленных на открытом огне.",
                "rating": 4.4,
                "image_url": "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=600&h=400&fit=crop",
                "opening_time": time(12, 0),  # 12:00
                "closing_time": time(23, 0),  # 23:00
                "slot_duration": 120,  # 2 часа
                "gallery": [
                    "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop"
                ],
                "menu_images": [
                    "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop"
                ]
            },
            {
                "name": "Морская Волна",
                "location": "Владивосток, ул. Набережная, 15",
                "latitude": 43.1178,
                "longitude": 131.8821,
                "cuisine": "Морепродукты",
                "price_range": "Средний",
                "description": "Ресторан с панорамным видом на море. Специализация на морепродуктах и рыбе. Свежие устрицы, мидии, крабы и рыба. Романтическая атмосфера и вид на закат.",
                "rating": 4.1,
                "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=600&h=400&fit=crop",
                "opening_time": time(10, 0),  # 10:00
                "closing_time": time(22, 0),  # 22:00
                "slot_duration": 90,  # 1.5 часа
                "gallery": [
                    "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop"
                ],
                "menu_images": [
                    "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop"
                ]
            },
            {
                "name": "Панорама",
                "location": "Владивосток, ул. Светланская, 25",
                "latitude": 43.1201,
                "longitude": 131.8857,
                "cuisine": "Европейская",
                "price_range": "Высокий",
                "description": "Ресторан на крыше с панорамным видом на город и море. Европейская кухня и коктейли. Изысканные блюда и авторские коктейли. Идеальное место для особых случаев.",
                "rating": 4.8,
                "image_url": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&h=400&fit=crop",
                "opening_time": time(18, 0),  # 18:00
                "closing_time": time(23, 0),  # 23:00
                "slot_duration": 120,  # 2 часа
                "gallery": [
                    "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=600&h=400&fit=crop"
                ],
                "menu_images": [
                    "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=600&h=400&fit=crop"
                ]
            },
            {
                "name": "У Тихого Океана",
                "location": "Владивосток, ул. Адмирала Фокина, 10",
                "latitude": 43.1159,
                "longitude": 131.8848,
                "cuisine": "Морепродукты",
                "price_range": "Средний",
                "description": "Ресторан с видом на Тихий океан. Свежие морепродукты и традиционные блюда Дальнего Востока. Специализируется на крабах, креветках и местной рыбе.",
                "rating": 4.3,
                "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=600&h=400&fit=crop",
                "opening_time": time(10, 0),  # 10:00
                "closing_time": time(22, 0),  # 22:00
                "slot_duration": 90,  # 1.5 часа
                "gallery": [
                    "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop"
                ],
                "menu_images": [
                    "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop"
                ]
            },
            {
                "name": "Восток",
                "location": "Владивосток, ул. Алеутская, 20",
                "latitude": 43.1234,
                "longitude": 131.8902,
                "cuisine": "Азиатская",
                "price_range": "Средний",
                "description": "Ресторан азиатской кухни с блюдами из Китая, Японии и Кореи. Современный интерьер. Фьюжн-кухня с элементами традиционных азиатских рецептов.",
                "rating": 4.0,
                "image_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&h=400&fit=crop",
                "opening_time": time(11, 0),  # 11:00
                "closing_time": time(21, 0),  # 21:00
                "slot_duration": 90,  # 1.5 часа
                "gallery": [
                    "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop"
                ],
                "menu_images": [
                    "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop"
                ]
            },
            # Новые рестораны
            {
                "name": "Стейк Хаус",
                "location": "Владивосток, ул. Светланская, 35",
                "latitude": 43.1185,
                "longitude": 131.8862,
                "cuisine": "Стейк-хаус",
                "price_range": "Высокий",
                "description": "Премиальный стейк-хаус с мраморным мясом высшего качества. Специализируется на стейках из австралийской и американской говядины. Винотека с коллекцией премиальных вин.",
                "rating": 4.9,
                "image_url": "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=600&h=400&fit=crop",
                "opening_time": time(12, 0),  # 12:00
                "closing_time": time(23, 0),  # 23:00
                "slot_duration": 120,  # 2 часа
                "gallery": [
                    "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop"
                ],
                "menu_images": [
                    "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop"
                ]
            },
            {
                "name": "Корейский Сад",
                "location": "Владивосток, ул. Алеутская, 8",
                "latitude": 43.1218,
                "longitude": 131.8885,
                "cuisine": "Корейская",
                "price_range": "Средний",
                "description": "Аутентичный корейский ресторан с традиционными блюдами. Кимчи, бибимбап, пулькоги и другие классические корейские блюда. Интерьер в традиционном корейском стиле.",
                "rating": 4.4,
                "image_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&h=400&fit=crop",
                "opening_time": time(11, 0),  # 11:00
                "closing_time": time(21, 30),  # 21:30
                "slot_duration": 90,  # 1.5 часа
                "gallery": [
                    "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop"
                ],
                "menu_images": [
                    "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop"
                ]
            },
            {
                "name": "Пиццерия Домино",
                "location": "Владивосток, ул. Семеновская, 25",
                "latitude": 43.1227,
                "longitude": 131.8869,
                "cuisine": "Пицца",
                "price_range": "Низкий",
                "description": "Современная пиццерия с дровяной печью. Классические и авторские пиццы, паста, салаты. Быстрое обслуживание и демократичные цены. Идеально для семейного ужина.",
                "rating": 4.2,
                "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&h=400&fit=crop",
                "opening_time": time(10, 0),  # 10:00
                "closing_time": time(22, 0),  # 22:00
                "slot_duration": 90,  # 1.5 часа
                "gallery": [
                    "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop"
                ],
                "menu_images": [
                    "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop"
                ]
            },
            {
                "name": "Веган Гарден",
                "location": "Владивосток, ул. Фокина, 15",
                "latitude": 43.1172,
                "longitude": 131.8851,
                "cuisine": "Веганская",
                "price_range": "Средний",
                "description": "Ресторан веганской кухни с органическими продуктами. Инновационные блюда без мяса и молочных продуктов. Здоровое питание и экологичный подход.",
                "rating": 4.6,
                "image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop",
                "opening_time": time(10, 0),  # 10:00
                "closing_time": time(22, 0),  # 22:00
                "slot_duration": 90,  # 1.5 часа
                "gallery": [
                    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&h=400&fit=crop"
                ],
                "menu_images": [
                    "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop"
                ]
            },
            {
                "name": "Барбекю Мастер",
                "location": "Владивосток, ул. Набережная, 25",
                "latitude": 43.1165,
                "longitude": 131.8818,
                "cuisine": "Барбекю",
                "price_range": "Средний",
                "description": "Ресторан барбекю с коптильнями и грилями. Свиные ребрышки, брисket, колбаски и другие блюда в стиле американского барбекю. Уютная атмосфера и большие порции.",
                "rating": 4.3,
                "image_url": "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=600&h=400&fit=crop",
                "opening_time": time(12, 0),  # 12:00
                "closing_time": time(23, 0),  # 23:00
                "slot_duration": 120,  # 2 часа
                "gallery": [
                    "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop"
                ],
                "menu_images": [
                    "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop"
                ]
            },
            {
                "name": "Суши Бар",
                "location": "Владивосток, ул. Адмирала Фокина, 5",
                "latitude": 43.1163,
                "longitude": 131.8842,
                "cuisine": "Суши",
                "price_range": "Средний",
                "description": "Современный суши-бар с конвейерной лентой. Свежие суши, роллы и сашими. Быстрое обслуживание и демократичные цены. Идеально для быстрого обеда.",
                "rating": 4.1,
                "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=600&h=400&fit=crop",
                "opening_time": time(10, 0),  # 10:00
                "closing_time": time(22, 0),  # 22:00
                "slot_duration": 90,  # 1.5 часа
                "gallery": [
                    "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop"
                ],
                "menu_images": [
                    "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop"
                ]
            },
            {
                "name": "Кафе Центральное",
                "location": "Владивосток, ул. Светланская, 10",
                "latitude": 43.1192,
                "longitude": 131.8865,
                "cuisine": "Кафе",
                "price_range": "Низкий",
                "description": "Уютное кафе в центре города. Завтраки, обеды, кофе и десерты. Европейская кухня и домашняя атмосфера. Идеально для встреч с друзьями и работы.",
                "rating": 4.0,
                "image_url": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&h=400&fit=crop",
                "opening_time": time(10, 0),  # 10:00
                "closing_time": time(22, 0),  # 22:00
                "slot_duration": 90,  # 1.5 часа
                "gallery": [
                    "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop"
                ],
                "menu_images": [
                    "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=600&h=400&fit=crop"
                ]
            }
        ]

        # --- ГАРАНТИЯ: gallery и menu_images всегда списки ---
        for r in restaurants_data:
            if isinstance(r.get("gallery"), str):
                r["gallery"] = [url.strip() for url in r["gallery"].split(",") if url.strip()]
            if isinstance(r.get("menu_images"), str):
                r["menu_images"] = [url.strip() for url in r["menu_images"].split(",") if url.strip()]

        for restaurant_data in restaurants_data:
            # Проверяем, нет ли уже такого ресторана
            exists = db.query(Restaurant).filter(Restaurant.name == restaurant_data["name"]).first()
            if not exists:
                db_restaurant = Restaurant(**restaurant_data, owner_id=admin.id)
                db.add(db_restaurant)
                db.commit()
                db.refresh(db_restaurant)
                print(f"Добавлен ресторан: {db_restaurant.name}")

        print(f"Обработано {len(restaurants_data)} ресторанов Владивостока")
    except Exception as e:
        print(f"Ошибка при сидировании: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed_restaurants() 