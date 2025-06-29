"use client";
import { useAuth } from "@/shared/store";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import api from "../../shared/api";
import styles from "./admin.module.css";
import Footer from "../components/Footer";

export default function AdminPage() {
    const { user } = useAuth();
    const router = useRouter();
    const [activeTab, setActiveTab] = useState("restaurants");
    const [restaurants, setRestaurants] = useState([]);
    const [bookings, setBookings] = useState([]);
    const [tables, setTables] = useState([]);
    const [loading, setLoading] = useState(true);
    const [newRestaurant, setNewRestaurant] = useState({
        name: "",
        location: "",
        cuisine: "",
        price_range: "",
        description: ""
    });
    const [newTable, setNewTable] = useState({
        restaurant_id: "",
        seats: 2,
        is_available: true
    });

    useEffect(() => {
        if (!user || user.role !== "admin") {
            router.push("/login");
            return;
        }
        fetchData();
    }, [user, router]);

    const fetchData = async () => {
        try {
            const bookingsUrl = user && user.role === "admin" ? "/bookings/all" : "/bookings/";
            const [restaurantsRes, bookingsRes, tablesRes] = await Promise.all([
                api.get("/restaurants/"),
                api.get(bookingsUrl),
                api.get("/tables/")
            ]);
            setRestaurants(restaurantsRes.data);
            setBookings(bookingsRes.data);
            setTables(tablesRes.data);
        } catch (error) {
            console.error("Error fetching data:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleCreateRestaurant = async (e) => {
        e.preventDefault();
        try {
            await api.post("/restaurants/", newRestaurant);
            setNewRestaurant({
                name: "",
                location: "",
                cuisine: "",
                price_range: "",
                description: ""
            });
            fetchData();
        } catch (error) {
            // Ошибка обрабатывается автоматически
        }
    };

    const handleCreateTable = async (e) => {
        e.preventDefault();
        if (!newTable.restaurant_id) {
            return;
        }
        try {
            await api.post("/tables/", newTable);
            setNewTable({
                restaurant_id: "",
                seats: 2,
                is_available: true
            });
            fetchData();
        } catch (error) {
            // Ошибка обрабатывается автоматически
        }
    };

    const handleUpdateBookingStatus = async (bookingId, status) => {
        try {
            await api.put(`/bookings/${bookingId}`, { status });
            fetchData();
        } catch (error) {
            // Ошибка обрабатывается автоматически
        }
    };

    const handleToggleTableAvailability = async (tableId) => {
        try {
            await api.put(`/tables/${tableId}/availability`);
            fetchData();
        } catch (error) {
            // Ошибка обрабатывается автоматически
        }
    };

    const handleDeleteTable = async (tableId) => {
        if (!confirm("Вы уверены, что хотите удалить этот столик?")) {
            return;
        }
        try {
            await api.delete(`/tables/${tableId}`);
            fetchData();
        } catch (error) {
            // Ошибка обрабатывается автоматически
        }
    };

    const getRestaurantName = (restaurantId) => {
        const restaurant = restaurants.find(r => r.id === restaurantId);
        return restaurant ? restaurant.name : `Ресторан #${restaurantId}`;
    };

    if (!user || user.role !== "admin") {
        return (
            <div className={styles.container}>
                <div className={styles.loading}>Проверка прав доступа...</div>
            </div>
        );
    }

    if (loading) {
        return (
            <div className={styles.container}>
                <div className={styles.loading}>Загрузка данных...</div>
            </div>
        );
    }

    return (
        <>
            <div className={styles.background}></div>
            <div className={styles.container}>
                <div className={styles.header}>
                    <h1 className={styles.title}>Панель администратора</h1>
                </div>

                <div className={styles.tabs}>
                    <button 
                        className={`${styles.tab} ${activeTab === "restaurants" ? styles.activeTab : ""}`}
                        onClick={() => setActiveTab("restaurants")}
                    >
                        Рестораны
                    </button>
                    <button 
                        className={`${styles.tab} ${activeTab === "bookings" ? styles.activeTab : ""}`}
                        onClick={() => setActiveTab("bookings")}
                    >
                        Бронирования
                    </button>
                    <button 
                        className={`${styles.tab} ${activeTab === "tables" ? styles.activeTab : ""}`}
                        onClick={() => setActiveTab("tables")}
                    >
                        Столики
                    </button>
                </div>

                <div className={styles.content}>
                    {activeTab === "restaurants" && (
                        <div className={styles.section}>
                            <h2>Управление ресторанами</h2>
                            
                            {/* Форма создания ресторана */}
                            <div className={styles.createForm}>
                                <h3>Создать новый ресторан</h3>
                                <form onSubmit={handleCreateRestaurant}>
                                    <div className={styles.formGrid}>
                                        <input
                                            type="text"
                                            placeholder="Название ресторана"
                                            value={newRestaurant.name}
                                            onChange={(e) => setNewRestaurant({...newRestaurant, name: e.target.value})}
                                            required
                                            className={styles.input}
                                        />
                                        <input
                                            type="text"
                                            placeholder="Адрес"
                                            value={newRestaurant.location}
                                            onChange={(e) => setNewRestaurant({...newRestaurant, location: e.target.value})}
                                            required
                                            className={styles.input}
                                        />
                                        <input
                                            type="text"
                                            placeholder="Кухня"
                                            value={newRestaurant.cuisine}
                                            onChange={(e) => setNewRestaurant({...newRestaurant, cuisine: e.target.value})}
                                            required
                                            className={styles.input}
                                        />
                                        <select
                                            value={newRestaurant.price_range}
                                            onChange={(e) => setNewRestaurant({...newRestaurant, price_range: e.target.value})}
                                            required
                                            className={styles.select}
                                        >
                                            <option value="">Выберите ценовой диапазон</option>
                                            <option value="$">$ (Недорого)</option>
                                            <option value="$$">$$ (Средне)</option>
                                            <option value="$$$">$$$ (Дорого)</option>
                                            <option value="$$$$">$$$$ (Премиум)</option>
                                        </select>
                                        <input
                                            type="number"
                                            step="any"
                                            placeholder="Широта (latitude)"
                                            value={newRestaurant.latitude || ""}
                                            onChange={(e) => setNewRestaurant({...newRestaurant, latitude: e.target.value})}
                                            className={styles.input}
                                        />
                                        <input
                                            type="number"
                                            step="any"
                                            placeholder="Долгота (longitude)"
                                            value={newRestaurant.longitude || ""}
                                            onChange={(e) => setNewRestaurant({...newRestaurant, longitude: e.target.value})}
                                            className={styles.input}
                                        />
                                    </div>
                                    <textarea
                                        placeholder="Описание ресторана"
                                        value={newRestaurant.description}
                                        onChange={(e) => setNewRestaurant({...newRestaurant, description: e.target.value})}
                                        className={styles.textarea}
                                        rows="3"
                                    />
                                    <button type="submit" className={styles.submitButton}>
                                        Создать ресторан
                                    </button>
                                </form>
                            </div>

                            {/* Список ресторанов */}
                            <div className={styles.restaurantsList}>
                                <h3>Существующие рестораны</h3>
                                {restaurants.map(restaurant => (
                                    <div key={restaurant.id} className={styles.restaurantCard}>
                                        <div className={styles.restaurantInfo}>
                                            <h4>{restaurant.name}</h4>
                                            <p><strong>Адрес:</strong> {restaurant.location}</p>
                                            <p><strong>Координаты:</strong> {restaurant.latitude}, {restaurant.longitude}</p>
                                            <p><strong>Кухня:</strong> {restaurant.cuisine}</p>
                                            <p><strong>Цена:</strong> {restaurant.price_range}</p>
                                            <p><strong>Рейтинг:</strong> {restaurant.rating}</p>
                                        </div>
                                        <div className={styles.restaurantActions}>
                                            <button className={styles.editButton}>
                                                Редактировать
                                            </button>
                                            <button className={styles.deleteButton}>
                                                Удалить
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {activeTab === "bookings" && (
                        <div className={styles.section}>
                            <h2>Управление бронированиями</h2>
                            <div className={styles.bookingsList}>
                                {bookings.map(booking => (
                                    <div key={booking.id} className={styles.bookingCard}>
                                        <div className={styles.bookingInfo}>
                                            <h4>Бронирование #{booking.id}</h4>
                                            <p><strong>Ресторан:</strong> {booking.restaurant_name || `Ресторан #${booking.table_id}`}</p>
                                            <p><strong>Дата:</strong> {new Date(booking.date).toLocaleDateString()}</p>
                                            <p><strong>Время:</strong> {booking.time}</p>
                                            <p><strong>Гостей:</strong> {booking.guests_count}</p>
                                            <p><strong>Статус:</strong> {booking.status}</p>
                                        </div>
                                        <div className={styles.bookingActions}>
                                            {booking.status === "active" && (
                                                <>
                                                    <button 
                                                        className={styles.completeButton}
                                                        onClick={() => handleUpdateBookingStatus(booking.id, "completed")}
                                                    >
                                                        Завершить
                                                    </button>
                                                    <button 
                                                        className={styles.cancelButton}
                                                        onClick={() => handleUpdateBookingStatus(booking.id, "cancelled")}
                                                    >
                                                        Отменить
                                                    </button>
                                                </>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {activeTab === "tables" && (
                        <div className={styles.section}>
                            <h2>Управление столиками</h2>
                            
                            {/* Форма добавления столика */}
                            <div className={styles.createForm}>
                                <h3>Добавить новый столик</h3>
                                <form onSubmit={handleCreateTable}>
                                    <div className={styles.formGrid}>
                                        <select
                                            value={newTable.restaurant_id}
                                            onChange={(e) => setNewTable({...newTable, restaurant_id: parseInt(e.target.value)})}
                                            required
                                            className={styles.select}
                                        >
                                            <option value="">Выберите ресторан</option>
                                            {restaurants.map(restaurant => (
                                                <option key={restaurant.id} value={restaurant.id}>
                                                    {restaurant.name}
                                                </option>
                                            ))}
                                        </select>
                                        <input
                                            type="number"
                                            placeholder="Количество мест"
                                            min="1"
                                            max="20"
                                            value={newTable.seats}
                                            onChange={(e) => setNewTable({...newTable, seats: parseInt(e.target.value)})}
                                            required
                                            className={styles.input}
                                        />
                                        <label className={styles.checkboxLabel}>
                                            <input
                                                type="checkbox"
                                                checked={newTable.is_available}
                                                onChange={(e) => setNewTable({...newTable, is_available: e.target.checked})}
                                            />
                                            Доступен для бронирования
                                        </label>
                                    </div>
                                    <button type="submit" className={styles.submitButton}>
                                        Добавить столик
                                    </button>
                                </form>
                            </div>

                            {/* Список столиков */}
                            <div className={styles.tablesList}>
                                <h3>Существующие столики</h3>
                                {tables.map(table => (
                                    <div key={table.id} className={styles.tableCard}>
                                        <div className={styles.tableInfo}>
                                            <h4>Столик #{table.id}</h4>
                                            <p><strong>Ресторан:</strong> {getRestaurantName(table.restaurant_id)}</p>
                                            <p><strong>Мест:</strong> {table.seats}</p>
                                            <p><strong>Статус:</strong> 
                                                <span className={table.is_available ? styles.available : styles.unavailable}>
                                                    {table.is_available ? " Доступен" : " Недоступен"}
                                                </span>
                                            </p>
                                        </div>
                                        <div className={styles.tableActions}>
                                            <button 
                                                className={table.is_available ? styles.unavailableButton : styles.availableButton}
                                                onClick={() => handleToggleTableAvailability(table.id)}
                                            >
                                                {table.is_available ? "Сделать недоступным" : "Сделать доступным"}
                                            </button>
                                            <button 
                                                className={styles.deleteButton}
                                                onClick={() => handleDeleteTable(table.id)}
                                            >
                                                Удалить
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>
            <Footer />
        </>
    );
} 