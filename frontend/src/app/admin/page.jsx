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
    const [loading, setLoading] = useState(true);
    const [authLoading, setAuthLoading] = useState(true);
    const [editingRestaurant, setEditingRestaurant] = useState(null);
    const [newRestaurant, setNewRestaurant] = useState({
        name: "",
        location: "",
        latitude: "",
        longitude: "",
        cuisine: "",
        price_range: "",
        description: "",
        opening_time: "10:00",
        closing_time: "22:00",
        phone: "",
        image_url: "",
        gallery: [],
        menu_images: []
    });

    useEffect(() => {
        // Проверяем, есть ли токен в localStorage
        const token = localStorage.getItem("token");
        const userStr = localStorage.getItem("user");
        if (token && userStr) {
            setAuthLoading(false);
        } else {
            setAuthLoading(false);
            if (!user) {
                router.push("/login");
                return;
            }
        }
    }, []);

    useEffect(() => {
        if (!authLoading && user && user.role === "admin") {
            fetchData();
        } else if (!authLoading && (!user || user.role !== "admin")) {
            router.push("/login");
        }
        // eslint-disable-next-line
    }, [user, authLoading]);

    const fetchData = async () => {
        setLoading(true);
        try {
            const bookingsUrl = user.role === "admin" ? "/bookings/" : `/bookings/?user_id=${user.id}`;
            const [restaurantsRes, bookingsRes] = await Promise.all([
                api.get("/restaurants/"),
                api.get(bookingsUrl)
            ]);
            setRestaurants(restaurantsRes.data);
            setBookings(bookingsRes.data);
        } catch (error) {
        } finally {
            setLoading(false);
        }
    };

    const handleCreateRestaurant = async (e) => {
        e.preventDefault();
        try {
            const restaurantData = {
                ...newRestaurant,
                latitude: newRestaurant.latitude ? parseFloat(newRestaurant.latitude) : null,
                longitude: newRestaurant.longitude ? parseFloat(newRestaurant.longitude) : null,
                gallery: newRestaurant.gallery.filter(url => url.trim()),
                menu_images: newRestaurant.menu_images.filter(url => url.trim())
            };
            
            await api.post("/restaurants/", restaurantData);
            setNewRestaurant({
                name: "",
                location: "",
                latitude: "",
                longitude: "",
                cuisine: "",
                price_range: "",
                description: "",
                opening_time: "10:00",
                closing_time: "22:00",
                phone: "",
                image_url: "",
                gallery: [],
                menu_images: []
            });
            fetchData();
        } catch (error) {
        }
    };

    const handleUpdateRestaurant = async (e) => {
        e.preventDefault();
        if (!editingRestaurant) return;
        
        try {
            const restaurantData = {
                ...editingRestaurant,
                latitude: editingRestaurant.latitude ? parseFloat(editingRestaurant.latitude) : null,
                longitude: editingRestaurant.longitude ? parseFloat(editingRestaurant.longitude) : null,
                gallery: editingRestaurant.gallery.filter(url => url.trim()),
                menu_images: editingRestaurant.menu_images.filter(url => url.trim())
            };
            
            await api.put(`/restaurants/${editingRestaurant.id}`, restaurantData);
            setEditingRestaurant(null);
            fetchData();
        } catch (error) {
        }
    };

    const handleDeleteRestaurant = async (restaurantId) => {
        if (!confirm("Вы уверены, что хотите удалить этот ресторан?")) {
            return;
        }
        try {
            await api.delete(`/restaurants/${restaurantId}`);
            fetchData();
        } catch (error) {
        }
    };

    const handleUpdateBookingStatus = async (bookingId, status) => {
        try {
            await api.put(`/bookings/${bookingId}`, { status });
            fetchData();
        } catch (error) {
        }
    };

    const addImageUrl = (type, url) => {
        if (!url.trim()) return;
        
        if (editingRestaurant) {
            setEditingRestaurant({
                ...editingRestaurant,
                [type]: [...editingRestaurant[type], url.trim()]
            });
        } else {
            setNewRestaurant({
                ...newRestaurant,
                [type]: [...newRestaurant[type], url.trim()]
            });
        }
    };

    const removeImageUrl = (type, index) => {
        if (editingRestaurant) {
            setEditingRestaurant({
                ...editingRestaurant,
                [type]: editingRestaurant[type].filter((_, i) => i !== index)
            });
        } else {
            setNewRestaurant({
                ...newRestaurant,
                [type]: newRestaurant[type].filter((_, i) => i !== index)
            });
        }
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString("ru-RU");
    };

    const formatTime = (timeString) => {
        return timeString.substring(0, 5);
    };

    const getStatusText = (status) => {
        switch (status) {
            case "active": return "Активно";
            case "cancelled": return "Отменено";
            case "completed": return "Завершено";
            default: return status;
        }
    };

    const getStatusClass = (status) => {
        switch (status) {
            case "active": return styles.statusActive;
            case "cancelled": return styles.statusCancelled;
            case "completed": return styles.statusCompleted;
            default: return "";
        }
    };

    if (authLoading) {
        return (
            <div className={styles.container}>
                <div className={styles.loading}>Проверка авторизации...</div>
            </div>
        );
    }

    if (!user || user.role !== "admin") {
        return null;
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
                </div>

                <div className={styles.content}>
                    {activeTab === "restaurants" && (
                        <div className={styles.section}>
                            <h2>Управление ресторанами</h2>
                            
                            {/* Форма создания/редактирования ресторана */}
                            <div className={styles.createForm}>
                                <h3>{editingRestaurant ? "Редактировать ресторан" : "Создать новый ресторан"}</h3>
                                <form onSubmit={editingRestaurant ? handleUpdateRestaurant : handleCreateRestaurant}>
                                    <div className={styles.formGrid}>
                                        <input
                                            type="text"
                                            placeholder="Название ресторана"
                                            value={editingRestaurant ? editingRestaurant.name : newRestaurant.name}
                                            onChange={(e) => editingRestaurant 
                                                ? setEditingRestaurant({...editingRestaurant, name: e.target.value})
                                                : setNewRestaurant({...newRestaurant, name: e.target.value})
                                            }
                                            required
                                            className={styles.input}
                                        />
                                        <input
                                            type="text"
                                            placeholder="Адрес"
                                            value={editingRestaurant ? editingRestaurant.location : newRestaurant.location}
                                            onChange={(e) => editingRestaurant 
                                                ? setEditingRestaurant({...editingRestaurant, location: e.target.value})
                                                : setNewRestaurant({...newRestaurant, location: e.target.value})
                                            }
                                            required
                                            className={styles.input}
                                        />
                                        <input
                                            type="text"
                                            placeholder="Кухня"
                                            value={editingRestaurant ? editingRestaurant.cuisine : newRestaurant.cuisine}
                                            onChange={(e) => editingRestaurant 
                                                ? setEditingRestaurant({...editingRestaurant, cuisine: e.target.value})
                                                : setNewRestaurant({...newRestaurant, cuisine: e.target.value})
                                            }
                                            required
                                            className={styles.input}
                                        />
                                        <select
                                            value={editingRestaurant ? editingRestaurant.price_range : newRestaurant.price_range}
                                            onChange={(e) => editingRestaurant 
                                                ? setEditingRestaurant({...editingRestaurant, price_range: e.target.value})
                                                : setNewRestaurant({...newRestaurant, price_range: e.target.value})
                                            }
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
                                            value={editingRestaurant ? editingRestaurant.latitude || "" : newRestaurant.latitude}
                                            onChange={(e) => editingRestaurant 
                                                ? setEditingRestaurant({...editingRestaurant, latitude: e.target.value})
                                                : setNewRestaurant({...newRestaurant, latitude: e.target.value})
                                            }
                                            className={styles.input}
                                        />
                                        <input
                                            type="number"
                                            step="any"
                                            placeholder="Долгота (longitude)"
                                            value={editingRestaurant ? editingRestaurant.longitude || "" : newRestaurant.longitude}
                                            onChange={(e) => editingRestaurant 
                                                ? setEditingRestaurant({...editingRestaurant, longitude: e.target.value})
                                                : setNewRestaurant({...newRestaurant, longitude: e.target.value})
                                            }
                                            className={styles.input}
                                        />
                                        <input
                                            type="time"
                                            value={editingRestaurant ? editingRestaurant.opening_time : newRestaurant.opening_time}
                                            onChange={(e) => editingRestaurant 
                                                ? setEditingRestaurant({...editingRestaurant, opening_time: e.target.value})
                                                : setNewRestaurant({...newRestaurant, opening_time: e.target.value})
                                            }
                                            className={styles.input}
                                        />
                                        <input
                                            type="time"
                                            value={editingRestaurant ? editingRestaurant.closing_time : newRestaurant.closing_time}
                                            onChange={(e) => editingRestaurant 
                                                ? setEditingRestaurant({...editingRestaurant, closing_time: e.target.value})
                                                : setNewRestaurant({...newRestaurant, closing_time: e.target.value})
                                            }
                                            className={styles.input}
                                        />
                                        <input
                                            type="tel"
                                            placeholder="Телефон"
                                            value={editingRestaurant ? editingRestaurant.phone || "" : newRestaurant.phone}
                                            onChange={(e) => editingRestaurant 
                                                ? setEditingRestaurant({...editingRestaurant, phone: e.target.value})
                                                : setNewRestaurant({...newRestaurant, phone: e.target.value})
                                            }
                                            className={styles.input}
                                        />
                                    </div>
                                    <textarea
                                        placeholder="Описание ресторана"
                                        value={editingRestaurant ? editingRestaurant.description || "" : newRestaurant.description}
                                        onChange={(e) => editingRestaurant 
                                            ? setEditingRestaurant({...editingRestaurant, description: e.target.value})
                                            : setNewRestaurant({...newRestaurant, description: e.target.value})
                                        }
                                        className={styles.textarea}
                                        rows="3"
                                    />
                                    
                                    {/* Главное изображение */}
                                    <div className={styles.imageSection}>
                                        <h4>Главное изображение</h4>
                                        <div className={styles.imageInput}>
                                            <input
                                                type="url"
                                                placeholder="URL главного изображения"
                                                value={editingRestaurant ? editingRestaurant.image_url || "" : newRestaurant.image_url}
                                                onChange={(e) => editingRestaurant 
                                                    ? setEditingRestaurant({...editingRestaurant, image_url: e.target.value})
                                                    : setNewRestaurant({...newRestaurant, image_url: e.target.value})
                                                }
                                                className={styles.input}
                                            />
                                            {editingRestaurant && (
                                                <input
                                                    type="file"
                                                    accept="image/*"
                                                    onChange={async (e) => {
                                                        const file = e.target.files[0];
                                                        if (file) {
                                                            const formData = new FormData();
                                                            formData.append('file', file);
                                                            try {
                                                                const response = await api.post(`/restaurants/${editingRestaurant.id}/upload_main_image`, formData, {
                                                                    headers: { 'Content-Type': 'multipart/form-data' }
                                                                });
                                                                setEditingRestaurant({
                                                                    ...editingRestaurant,
                                                                    image_url: response.data.image_url
                                                                });
                                                            } catch (error) {
                                                            }
                                                        }
                                                    }}
                                                    className={styles.fileInput}
                                                />
                                            )}
                                        </div>
                                        <p className={styles.helpText}>
                                            {editingRestaurant 
                                                ? "Или загрузите файл (автоматически сохранится как main.jpg)"
                                                : "Для нового ресторана используйте URL или загрузите файл после создания"
                                            }
                                        </p>
                                    </div>

                                    {/* Галерея изображений */}
                                    <div className={styles.imageSection}>
                                        <h4>Галерея изображений</h4>
                                        <div className={styles.imageInput}>
                                            <input
                                                type="url"
                                                placeholder="URL изображения галереи"
                                                id="galleryUrl"
                                                className={styles.input}
                                            />
                                            <button
                                                type="button"
                                                onClick={() => {
                                                    const url = document.getElementById('galleryUrl').value;
                                                    addImageUrl('gallery', url);
                                                    document.getElementById('galleryUrl').value = '';
                                                }}
                                                className={styles.addButton}
                                            >
                                                Добавить URL
                                            </button>
                                            {editingRestaurant && (
                                                <input
                                                    type="file"
                                                    accept="image/*"
                                                    onChange={async (e) => {
                                                        const file = e.target.files[0];
                                                        if (file) {
                                                            const formData = new FormData();
                                                            formData.append('file', file);
                                                            try {
                                                                const response = await api.post(`/restaurants/${editingRestaurant.id}/upload_gallery_image`, formData, {
                                                                    headers: { 'Content-Type': 'multipart/form-data' }
                                                                });
                                                                setEditingRestaurant({
                                                                    ...editingRestaurant,
                                                                    gallery: [...(editingRestaurant.gallery || []), response.data.image_url]
                                                                });
                                                            } catch (error) {
                                                            }
                                                        }
                                                    }}
                                                    className={styles.fileInput}
                                                />
                                            )}
                                        </div>
                                        <div className={styles.imageList}>
                                            {(editingRestaurant ? editingRestaurant.gallery : newRestaurant.gallery).map((url, index) => (
                                                <div key={index} className={styles.imageItem}>
                                                    <span>{url}</span>
                                                    <button
                                                        type="button"
                                                        onClick={() => removeImageUrl('gallery', index)}
                                                        className={styles.removeButton}
                                                    >
                                                        ✕
                                                    </button>
                                                </div>
                                            ))}
                                        </div>
                                        <p className={styles.helpText}>
                                            {editingRestaurant 
                                                ? "Добавьте URL или загрузите файл (автоматически сохранится как gallery_X.jpg)"
                                                : "Для нового ресторана используйте URL или загрузите файл после создания"
                                            }
                                        </p>
                                    </div>

                                    {/* Изображения меню */}
                                    <div className={styles.imageSection}>
                                        <h4>Изображения меню</h4>
                                        <div className={styles.imageInput}>
                                            <input
                                                type="url"
                                                placeholder="URL изображения меню"
                                                id="menuUrl"
                                                className={styles.input}
                                            />
                                            <button
                                                type="button"
                                                onClick={() => {
                                                    const url = document.getElementById('menuUrl').value;
                                                    addImageUrl('menu_images', url);
                                                    document.getElementById('menuUrl').value = '';
                                                }}
                                                className={styles.addButton}
                                            >
                                                Добавить URL
                                            </button>
                                            {editingRestaurant && (
                                                <input
                                                    type="file"
                                                    accept="image/*"
                                                    onChange={async (e) => {
                                                        const file = e.target.files[0];
                                                        if (file) {
                                                            const formData = new FormData();
                                                            formData.append('file', file);
                                                            try {
                                                                const response = await api.post(`/restaurants/${editingRestaurant.id}/upload_menu_image`, formData, {
                                                                    headers: { 'Content-Type': 'multipart/form-data' }
                                                                });
                                                                setEditingRestaurant({
                                                                    ...editingRestaurant,
                                                                    menu_images: [...(editingRestaurant.menu_images || []), response.data.image_url]
                                                                });
                                                            } catch (error) {
                                                            }
                                                        }
                                                    }}
                                                    className={styles.fileInput}
                                                />
                                            )}
                                        </div>
                                        <div className={styles.imageList}>
                                            {(editingRestaurant ? editingRestaurant.menu_images : newRestaurant.menu_images).map((url, index) => (
                                                <div key={index} className={styles.imageItem}>
                                                    <span>{url}</span>
                                                    <button
                                                        type="button"
                                                        onClick={() => removeImageUrl('menu_images', index)}
                                                        className={styles.removeButton}
                                                    >
                                                        ✕
                                                    </button>
                                                </div>
                                            ))}
                                        </div>
                                        <p className={styles.helpText}>
                                            {editingRestaurant 
                                                ? "Добавьте URL или загрузите файл (автоматически сохранится как menu_X.jpg)"
                                                : "Для нового ресторана используйте URL или загрузите файл после создания"
                                            }
                                        </p>
                                    </div>

                                    <div className={styles.formActions}>
                                        <button type="submit" className={styles.submitButton}>
                                            {editingRestaurant ? "Обновить ресторан" : "Создать ресторан"}
                                        </button>
                                        {editingRestaurant && (
                                            <button
                                                type="button"
                                                onClick={() => setEditingRestaurant(null)}
                                                className={styles.cancelButton}
                                            >
                                                Отменить редактирование
                                            </button>
                                        )}
                                    </div>
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
                                            <p><strong>Время работы:</strong> {restaurant.opening_time} - {restaurant.closing_time}</p>
                                            <p><strong>Телефон:</strong> {restaurant.phone || "Не указан"}</p>
                                            <p><strong>Описание:</strong> {restaurant.description || "Не указано"}</p>
                                            <p><strong>Главное изображение:</strong> {restaurant.image_url || "Не указано"}</p>
                                            <p><strong>Галерея:</strong> {restaurant.gallery?.length || 0} изображений</p>
                                            <p><strong>Меню:</strong> {restaurant.menu_images?.length || 0} изображений</p>
                                        </div>
                                        <div className={styles.restaurantActions}>
                                            <button 
                                                className={styles.editButton}
                                                onClick={() => setEditingRestaurant(restaurant)}
                                            >
                                                Редактировать
                                            </button>
                                            <button 
                                                className={styles.deleteButton}
                                                onClick={() => handleDeleteRestaurant(restaurant.id)}
                                            >
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
                                            <p><strong>Дата:</strong> {formatDate(booking.date)}</p>
                                            <p><strong>Время:</strong> {formatTime(booking.time)}</p>
                                            <p><strong>Гостей:</strong> {booking.guests_count}</p>
                                            <p><strong>Столик:</strong> #{booking.table_id}</p>
                                            <p><strong>Статус:</strong> 
                                                <span className={`${styles.status} ${getStatusClass(booking.status)}`}>
                                                    {getStatusText(booking.status)}
                                                </span>
                                            </p>
                                            <p><strong>Пользователь:</strong> {booking.user_email || "Не указан"}</p>
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
                </div>
            </div>
            <Footer />
        </>
    );
} 