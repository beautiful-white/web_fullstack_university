"use client";
import { useEffect, useState } from "react";
import api from "../../../shared/api";
import { useParams, useRouter } from "next/navigation";
import { useAuth } from "../../../shared/store";
import styles from "./restaurant-detail.module.css";

export default function RestaurantDetailPage() {
    const params = useParams();
    const router = useRouter();
    const { user } = useAuth();
    const [restaurant, setRestaurant] = useState(null);
    const [loading, setLoading] = useState(true);
    const [availableTables, setAvailableTables] = useState([]);
    const [loadingTables, setLoadingTables] = useState(false);
    const [bookingData, setBookingData] = useState({
        date: "",
        time: "",
        guests: 2,
        table_id: null
    });

    useEffect(() => {
        fetchRestaurant();
    }, [params.id]);

    const fetchRestaurant = async () => {
        try {
            const response = await api.get(`/restaurants/${params.id}`);
            setRestaurant(response.data);
        } catch (error) {
            console.error("Error fetching restaurant:", error);
        } finally {
            setLoading(false);
        }
    };

    const fetchAvailableTables = async () => {
        if (!bookingData.date || !bookingData.time || !bookingData.guests) {
            return;
        }

        setLoadingTables(true);
        try {
            const response = await api.get(`/restaurants/${params.id}/available-tables`, {
                params: {
                    date: bookingData.date,
                    time: bookingData.time,
                    guests: bookingData.guests
                }
            });
            setAvailableTables(response.data.available_tables);
        } catch (error) {
            console.error("Error fetching available tables:", error);
            setAvailableTables([]);
        } finally {
            setLoadingTables(false);
        }
    };

    useEffect(() => {
        fetchAvailableTables();
    }, [bookingData.date, bookingData.time, bookingData.guests]);

    const handleBooking = async (e) => {
        e.preventDefault();
        if (!user) {
            router.push("/login");
            return;
        }

        if (!bookingData.table_id) {
            alert("Пожалуйста, выберите столик");
            return;
        }

        try {
            await api.post("/bookings/", {
                table_id: bookingData.table_id,
                date: bookingData.date,
                time: bookingData.time,
                guests_count: bookingData.guests
            });
            alert("Бронирование успешно создано!");
            router.push("/bookings");
        } catch (error) {
            if (error.response?.data?.detail) {
                alert(error.response.data.detail);
            } else {
                alert("Ошибка при создании бронирования");
            }
        }
    };

    const renderStars = (rating) => {
        const stars = [];
        for (let i = 1; i <= 5; i++) {
            stars.push(
                <span key={i} className={i <= rating ? styles.starFilled : styles.starEmpty}>
                    ★
                </span>
            );
        }
        return stars;
    };

    if (loading) {
        return (
            <div className={styles.container}>
                <div className={styles.loading}>Загрузка ресторана...</div>
            </div>
        );
    }

    if (!restaurant) {
        return (
            <div className={styles.container}>
                <div className={styles.error}>Ресторан не найден</div>
            </div>
        );
    }

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <button className={styles.backButton} onClick={() => router.back()}>
                    ← Назад
                </button>
            </div>

            <div className={styles.content}>
                <div className={styles.imageSection}>
                    <img 
                        src={restaurant.image_url || "https://via.placeholder.com/600x400?text=Ресторан"} 
                        alt={restaurant.name}
                        className={styles.restaurantImage}
                    />
                </div>

                <div className={styles.infoSection}>
                    <h1 className={styles.restaurantName}>{restaurant.name}</h1>
                    <p className={styles.description}>{restaurant.description}</p>
                    
                    <div className={styles.details}>
                        <div className={styles.detail}>
                            <span className={styles.label}>Кухня:</span>
                            <span className={styles.value}>{restaurant.cuisine}</span>
                        </div>
                        <div className={styles.detail}>
                            <span className={styles.label}>Ценовой диапазон:</span>
                            <span className={styles.value}>{restaurant.price_range}</span>
                        </div>
                        <div className={styles.detail}>
                            <span className={styles.label}>Адрес:</span>
                            <span className={styles.value}>{restaurant.address}</span>
                        </div>
                        <div className={styles.detail}>
                            <span className={styles.label}>Рейтинг:</span>
                            <div className={styles.rating}>
                                {renderStars(restaurant.rating)}
                                <span className={styles.ratingText}>({restaurant.rating})</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className={styles.bookingSection}>
                <h2 className={styles.bookingTitle}>Забронировать столик</h2>
                <form onSubmit={handleBooking} className={styles.bookingForm}>
                    <div className={styles.formGroup}>
                        <label htmlFor="date">Дата</label>
                        <input
                            type="date"
                            id="date"
                            value={bookingData.date}
                            onChange={(e) => setBookingData({...bookingData, date: e.target.value, table_id: null})}
                            required
                            className={styles.input}
                            min={new Date().toISOString().split('T')[0]}
                        />
                    </div>
                    
                    <div className={styles.formGroup}>
                        <label htmlFor="time">Время</label>
                        <input
                            type="time"
                            id="time"
                            value={bookingData.time}
                            onChange={(e) => setBookingData({...bookingData, time: e.target.value, table_id: null})}
                            required
                            className={styles.input}
                        />
                    </div>
                    
                    <div className={styles.formGroup}>
                        <label htmlFor="guests">Количество гостей</label>
                        <select
                            id="guests"
                            value={bookingData.guests}
                            onChange={(e) => setBookingData({...bookingData, guests: parseInt(e.target.value), table_id: null})}
                            className={styles.select}
                        >
                            {[1,2,3,4,5,6,7,8].map(num => (
                                <option key={num} value={num}>{num} {num === 1 ? 'гость' : num < 5 ? 'гостя' : 'гостей'}</option>
                            ))}
                        </select>
                    </div>
                </form>

                {/* Выбор столика */}
                {bookingData.date && bookingData.time && (
                    <div className={styles.tablesSection}>
                        <h3 className={styles.tablesTitle}>Доступные столики</h3>
                        {loadingTables ? (
                            <div className={styles.loadingTables}>Поиск доступных столиков...</div>
                        ) : availableTables.length > 0 ? (
                            <div className={styles.tablesGrid}>
                                {availableTables.map(table => (
                                    <div 
                                        key={table.id} 
                                        className={`${styles.tableCard} ${bookingData.table_id === table.id ? styles.selectedTable : ''}`}
                                        onClick={() => setBookingData({...bookingData, table_id: table.id})}
                                    >
                                        <div className={styles.tableNumber}>Столик {table.id}</div>
                                        <div className={styles.tableSeats}>{table.seats} мест</div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className={styles.noTables}>
                                Нет доступных столиков на выбранное время
                            </div>
                        )}
                    </div>
                )}
                
                <button 
                    type="submit" 
                    className={styles.bookingButton}
                    onClick={handleBooking}
                    disabled={!bookingData.table_id}
                >
                    Забронировать
                </button>
            </div>
        </div>
    );
} 