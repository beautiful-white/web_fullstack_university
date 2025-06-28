"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "../../shared/store";
import api from "../../shared/api";
import styles from "./bookings.module.css";

export default function BookingsPage() {
    const [bookings, setBookings] = useState([]);
    const [loading, setLoading] = useState(true);
    const { user } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!user) {
            router.push("/login");
            return;
        }
        fetchBookings();
    }, [user]);

    const fetchBookings = async () => {
        try {
            const response = await api.get("/bookings/");
            setBookings(response.data);
        } catch (error) {
            console.error("Error fetching bookings:", error);
        } finally {
            setLoading(false);
        }
    };

    const cancelBooking = async (bookingId) => {
        if (!confirm("Вы уверены, что хотите отменить это бронирование?")) {
            return;
        }

        try {
            await api.delete(`/bookings/${bookingId}`);
            alert("Бронирование отменено");
            fetchBookings();
        } catch (error) {
            alert("Ошибка при отмене бронирования");
        }
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString("ru-RU");
    };

    const formatTime = (timeString) => {
        return timeString.substring(0, 5);
    };

    const getStatusText = (status) => {
        switch (status) {
            case "active":
                return "Активно";
            case "cancelled":
                return "Отменено";
            case "completed":
                return "Завершено";
            default:
                return status;
        }
    };

    const getStatusClass = (status) => {
        switch (status) {
            case "active":
                return styles.statusActive;
            case "cancelled":
                return styles.statusCancelled;
            case "completed":
                return styles.statusCompleted;
            default:
                return "";
        }
    };

    if (!user) {
        return null;
    }

    if (loading) {
        return (
            <div className={styles.container}>
                <div className={styles.loading}>Загрузка бронирований...</div>
            </div>
        );
    }

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h1 className={styles.title}>Мои бронирования</h1>
                <button 
                    className={styles.newBookingButton}
                    onClick={() => router.push("/restaurants")}
                >
                    Новое бронирование
                </button>
            </div>

            {bookings.length === 0 ? (
                <div className={styles.emptyState}>
                    <div className={styles.emptyIcon}>📅</div>
                    <h2 className={styles.emptyTitle}>У вас пока нет бронирований</h2>
                    <p className={styles.emptyText}>
                        Забронируйте столик в любимом ресторане прямо сейчас!
                    </p>
                    <button 
                        className={styles.emptyButton}
                        onClick={() => router.push("/restaurants")}
                    >
                        Найти ресторан
                    </button>
                </div>
            ) : (
                <div className={styles.bookingsGrid}>
                    {bookings.map((booking) => (
                        <div key={booking.id} className={styles.bookingCard}>
                            <div className={styles.bookingHeader}>
                                <h3 className={styles.restaurantName}>
                                    {booking.restaurant_name || `Ресторан #${booking.table_id}`}
                                </h3>
                                <span className={`${styles.status} ${getStatusClass(booking.status)}`}>
                                    {getStatusText(booking.status)}
                                </span>
                            </div>
                            
                            <div className={styles.bookingDetails}>
                                <div className={styles.detail}>
                                    <span className={styles.label}>Дата:</span>
                                    <span className={styles.value}>{formatDate(booking.date)}</span>
                                </div>
                                <div className={styles.detail}>
                                    <span className={styles.label}>Время:</span>
                                    <span className={styles.value}>{formatTime(booking.time)}</span>
                                </div>
                                <div className={styles.detail}>
                                    <span className={styles.label}>Гостей:</span>
                                    <span className={styles.value}>{booking.guests_count}</span>
                                </div>
                                <div className={styles.detail}>
                                    <span className={styles.label}>Столик:</span>
                                    <span className={styles.value}>
                                        #{booking.table_id} ({booking.table_seats || "N/A"} мест)
                                    </span>
                                </div>
                            </div>
                            
                            {booking.status === "active" && (
                                <div className={styles.bookingActions}>
                                    <button 
                                        className={styles.cancelButton}
                                        onClick={() => cancelBooking(booking.id)}
                                    >
                                        Отменить
                                    </button>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
} 