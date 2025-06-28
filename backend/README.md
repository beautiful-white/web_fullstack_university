# Backend — Restaurant Booking API

## Быстрый старт

1. Перейдите в папку backend:
   ```sh
   cd backend
   ```
2. Активируйте виртуальное окружение:
   - Для fish shell:
     ```sh
     source venv/bin/activate.fish
     ```
   - Для bash/zsh:
     ```sh
     source venv/bin/activate
     ```
3. Установите зависимости (если не установлены):
   ```sh
   pip install -r requirements.txt
   ```
4. Запустите сервер:
   ```sh
   uvicorn main:app --reload
   ```

## Структура
- `main.py` — точка входа FastAPI
- `venv/` — виртуальное окружение Python

## Требования
- Python 3.9+

---

## TODO
- Модели пользователей, ресторанов, бронирований
- CRUD-роуты
- Аутентификация 