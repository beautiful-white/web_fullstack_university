from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, restaurant, table, booking, auth, review


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user.router)
app.include_router(restaurant.router)
app.include_router(table.router)
app.include_router(booking.router)
app.include_router(review.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Restaurant Booking API!"}
