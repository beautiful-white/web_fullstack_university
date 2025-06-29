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
    
    # Начинаем с времени открытия
    current_time = restaurant.opening_time
    
    # Пока не достигнем времени закрытия
    while current_time < restaurant.closing_time:
        # Вычисляем время окончания слота
        start_minutes = current_time.hour * 60 + current_time.minute
        end_minutes = start_minutes + restaurant.slot_duration
        
        # Проверяем, не выходит ли слот за время работы ресторана
        if end_minutes > restaurant.closing_time.hour * 60 + restaurant.closing_time.minute:
            break
            
        end_time = time(hour=end_minutes // 60, minute=end_minutes % 60)
        
        # Создаем слот
        slot = TimeSlot(
            start_time=current_time,
            end_time=end_time,
            is_available=True  # По умолчанию доступен
        )
        slots.append(slot)
        
        # Переходим к следующему слоту
        next_minutes = start_minutes + restaurant.slot_duration
        current_time = time(hour=next_minutes // 60, minute=next_minutes % 60)
    
    return slots


def check_slot_availability(restaurant: Restaurant, date: datetime.date, 
                          start_time: time, end_time: time, db) -> bool:
    """
    Проверяет доступность временного слота для бронирования.
    Возвращает True, если слот доступен.
    """
    # Проверяем, есть ли активные брони на это время для столиков этого ресторана
    active_bookings = db.query(Booking).join(Table).filter(
        Table.restaurant_id == restaurant.id,
        Booking.date == date,
        Booking.time == start_time,
        Booking.status == "active"
    ).count()
    
    # Если есть активные брони, слот недоступен
    return active_bookings == 0


def get_available_time_slots(restaurant: Restaurant, date: datetime.date, 
                           guests: int, db) -> List[TimeSlot]:
    """
    Возвращает список доступных временных слотов для указанного количества гостей.
    """
    # Генерируем все возможные слоты
    all_slots = generate_time_slots(restaurant, date)
    
    # Проверяем доступность каждого слота
    available_slots = []
    for slot in all_slots:
        # Проверяем, есть ли столики с достаточной вместимостью
        suitable_tables = db.query(Table).filter(
            Table.restaurant_id == restaurant.id,
            Table.seats >= guests,
            Table.is_available == True
        ).count()
        
        if suitable_tables > 0:
            # Проверяем, не забронированы ли все подходящие столики на это время
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
                # Не добавляем недоступные слоты в результат
        else:
            slot.is_available = False
            # Не добавляем недоступные слоты в результат
    
    return available_slots 