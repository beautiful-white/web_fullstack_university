from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, restaurant, table, booking, auth, review


app = FastAPI()

# Настройка CORS - более подробная конфигурация
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Разрешаем запросы с фронтенда
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],  # Явно указываем методы
    allow_headers=["*"],  # Разрешаем все заголовки
    expose_headers=["*"],  # Разрешаем доступ к заголовкам ответа
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(user.router)
app.include_router(restaurant.router)
app.include_router(table.router)
app.include_router(booking.router)
app.include_router(review.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Restaurant Booking API!"}
