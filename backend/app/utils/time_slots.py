from datetime import time, timedelta, datetime
from typing import List
from app.models.restaurant import Restaurant
from app.models.booking import Booking
from app.models.table import Table
from app.schemas.booking import TimeSlot


def generate_time_slots(restaurant: Restaurant, date: datetime.date) -> List[TimeSlot]:
    """
    Генерирует временные слоты для ресторана на указанную дату.
    Слоты создаются с интервалом в slot_duration минут.
    """
    slots = []

    current_time = restaurant.opening_time

    while current_time < restaurant.closing_time:
        start_minutes = current_time.hour * 60 + current_time.minute
        end_minutes = start_minutes + restaurant.slot_duration

        if end_minutes > restaurant.closing_time.hour * 60 + restaurant.closing_time.minute:
            break
            
        end_time = time(hour=end_minutes // 60, minute=end_minutes % 60)

        slot = TimeSlot(
            start_time=current_time,
            end_time=end_time,
            is_available=True
        )
        slots.append(slot)
        

        next_minutes = start_minutes + restaurant.slot_duration
        current_time = time(hour=next_minutes // 60, minute=next_minutes % 60)
    
    return slots


def check_slot_availability(restaurant: Restaurant, date: datetime.date, 
                          start_time: time, end_time: time, db) -> bool:

    active_bookings = db.query(Booking).join(Table).filter(
        Table.restaurant_id == restaurant.id,
        Booking.date == date,
        Booking.time == start_time,
        Booking.status == "active"
    ).count()
    

    return active_bookings == 0


def get_available_time_slots(restaurant: Restaurant, date: datetime.date, 
                           guests: int, db) -> List[TimeSlot]:

    all_slots = generate_time_slots(restaurant, date)
    

    available_slots = []
    for slot in all_slots:

        suitable_tables = db.query(Table).filter(
            Table.restaurant_id == restaurant.id,
            Table.seats >= guests,
            Table.is_available == True
        ).count()
        
        if suitable_tables > 0:

            booked_tables = db.query(Booking).join(Table).filter(
                Table.restaurant_id == restaurant.id,
                Booking.date == date,
                Booking.time == slot.start_time,
                Booking.status == "active",
                Table.seats >= guests
            ).count()
            
            if booked_tables < suitable_tables:
                slot.is_available = True
                available_slots.append(slot)
            else:
                slot.is_available = False

        else:
            slot.is_available = False
    
    return available_slots 