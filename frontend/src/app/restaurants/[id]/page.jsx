"use client";
import { useEffect, useState } from "react";
import api from "../../../shared/api";
import { useParams, useRouter } from "next/navigation";
import { useAuth } from "../../../shared/store";
import styles from "./restaurant-detail.module.css";
import ReviewsSection from "./components/ReviewsSection";
import Footer from "../../components/Footer";

export default function RestaurantDetailPage() {
    const params = useParams();
    const router = useRouter();
    const { user } = useAuth();
    const [restaurant, setRestaurant] = useState(null);
    const [loading, setLoading] = useState(true);
    const [availableTables, setAvailableTables] = useState([]);
    const [loadingTables, setLoadingTables] = useState(false);
    const [activeImageIndex, setActiveImageIndex] = useState(0);
    const [activeMenuIndex, setActiveMenuIndex] = useState(0);
    const [availableTimeSlots, setAvailableTimeSlots] = useState([]);
    const [bookingData, setBookingData] = useState({
        date: "",
        time: "",
        guests: 2,
        table_id: null
    });

    const STATIC_BASE = "http://localhost:8000";

    useEffect(() => {
        fetchRestaurant();
    }, [params.id]);

    const fetchRestaurant = async () => {
        setLoading(true);
        try {
            const response = await api.get(`/restaurants/${params.id}`);
            setRestaurant(response.data);
        } catch (error) {
        } finally {
            setLoading(false);
        }
    };

    const fetchAvailableTimeSlots = async () => {
        if (!bookingData.date || !bookingData.guests) {
            setAvailableTimeSlots([]);
            setBookingData((prev) => ({ ...prev, time: "", table_id: null }));
            return;
        }
        try {
            const response = await api.get(`/restaurants/${params.id}/available-time-slots`, {
                params: {
                    date: bookingData.date,
                    guests: bookingData.guests
                }
            });
            
            setAvailableTimeSlots(response.data.time_slots);
            setBookingData((prev) => ({ ...prev, time: "", table_id: null }));
        } catch (error) {
            setAvailableTimeSlots([]);
            setBookingData((prev) => ({ ...prev, time: "", table_id: null }));
        }
    };

    useEffect(() => {
        fetchAvailableTimeSlots();
    }, [bookingData.date, bookingData.guests]);

    const fetchAvailableTables = async () => {
        if (!bookingData.date || !bookingData.time || !bookingData.guests) {
            setAvailableTables([]);
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
            setAvailableTables([]);
        } finally {
            setLoadingTables(false);
        }
    };

    useEffect(() => {
        if (bookingData.time) fetchAvailableTables();
    }, [bookingData.date, bookingData.time, bookingData.guests]);

    const handleBooking = async (e) => {
        e.preventDefault();
        if (!user) {
            router.push("/login");
            return;
        }
        if (!bookingData.table_id) {
            return;
        }
        try {
            await api.post("/bookings/", {
                table_id: bookingData.table_id,
                date: bookingData.date,
                time: bookingData.time,
                guests: bookingData.guests
            });
            router.push("/bookings");
        } catch (error) {
            if (error.response?.status === 401) {
                router.push("/login");
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

    const getGalleryImages = () => {
        if (!restaurant) return [];
        if (restaurant.gallery && Array.isArray(restaurant.gallery)) {
            return restaurant.gallery;
        }
        if (restaurant.gallery && typeof restaurant.gallery === 'string') {
            return restaurant.gallery.split(',').filter(url => url.trim());
        }
        return restaurant.image_url ? [restaurant.image_url] : [];
    };

    const getMenuImages = () => {
        if (!restaurant) return [];
        if (restaurant.menu_images && Array.isArray(restaurant.menu_images)) {
            return restaurant.menu_images;
        }
        if (restaurant.menu_images && typeof restaurant.menu_images === 'string') {
            return restaurant.menu_images.split(',').filter(url => url.trim());
        }
        return [];
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

    const galleryImages = getGalleryImages();
    const menuImages = getMenuImages();

    return (
        <>
            <div className={styles.background}></div>
            <div className={styles.container}>
                <div className={styles.header}>
                    <button className={styles.backButton} onClick={() => router.back()}>
                        ←
                    </button>
                </div>

                {/* Основная информация о ресторане */}
                <div className={styles.heroSection}>
                    <div className={styles.heroImage}>
                        <img 
                            src={restaurant.image_url ? `${STATIC_BASE}${restaurant.image_url}` : `${STATIC_BASE}/static/restaurants/images/default-restaurant.jpg`}
                            alt={restaurant.name}
                            className={styles.mainImage}
                        />
                        <div className={styles.heroOverlay}>
                            <h1 className={styles.restaurantName}>{restaurant.name}</h1>
                            <div className={styles.heroRating}>
                                {renderStars(restaurant.rating)}
                                <span className={styles.ratingText}>({restaurant.rating})</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div className={styles.content}>
                    <div className={styles.infoSection}>
                        <div className={styles.description}>
                            <h2>О ресторане</h2>
                            <p>{restaurant.description}</p>
                        </div>
                        
                        <div className={styles.details}>
                            <div className={styles.detail}>
                                <span className={styles.label}>Кухня:</span>
                                <span className={styles.value}>{restaurant.cuisine}</span>
                            </div>
                            <div className={styles.detail}>
                                <span className={styles.label}>Средний чек:</span>
                                <span className={styles.value}>{restaurant.price_range}</span>
                            </div>
                            <div className={styles.detail}>
                                <span className={styles.label}>Адрес:</span>
                                <span className={styles.value}>{restaurant.location}</span>
                            </div>
                            <div className={styles.detail}>
                                <span className={styles.label}>Время работы:</span>
                                <span className={styles.value}>
                                    {restaurant.opening_time && restaurant.closing_time 
                                        ? `${restaurant.opening_time.substring(0, 5)} - ${restaurant.closing_time.substring(0, 5)}`
                                        : '10:00 - 22:00'
                                    }
                                </span>
                            </div>
                            {restaurant.phone && (
                                <div className={styles.detail}>
                                    <span className={styles.label}>Телефон:</span>
                                    <span className={styles.value}>
                                        <a href={`tel:${restaurant.phone}`} className={styles.phoneLink}>
                                            {restaurant.phone}
                                        </a>
                                    </span>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Галерея фотографий */}
                    {galleryImages.length > 0 && (
                        <div className={styles.gallerySection}>
                            <h2>Фотографии ресторана</h2>
                            <div className={styles.gallery}>
                                <div className={styles.mainGalleryImage}>
                                    <img 
                                        src={`${STATIC_BASE}${galleryImages[activeImageIndex]}`}
                                        alt={`${restaurant.name} - фото ${activeImageIndex + 1}`}
                                        className={styles.galleryMainImage}
                                    />
                                </div>
                                {galleryImages.length > 1 && (
                                    <div className={styles.galleryThumbnails}>
                                        {galleryImages.map((image, index) => (
                                            <img 
                                                key={index}
                                                src={`${STATIC_BASE}${image}`}
                                                alt={`Фото ${index + 1}`}
                                                className={`${styles.galleryThumbnail} ${activeImageIndex === index ? styles.activeThumbnail : ''}`}
                                                onClick={() => setActiveImageIndex(index)}
                                            />
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    {/* Меню ресторана */}
                    {menuImages.length > 0 && (
                        <div className={styles.menuSection}>
                            <h2>Меню ресторана</h2>
                            <div className={styles.menuGallery}>
                                <div className={styles.mainMenuImage}>
                                    <img 
                                        src={`${STATIC_BASE}${menuImages[activeMenuIndex]}`}
                                        alt={`Меню ${activeMenuIndex + 1}`}
                                        className={styles.menuMainImage}
                                    />
                                </div>
                                {menuImages.length > 1 && (
                                    <div className={styles.menuThumbnails}>
                                        {menuImages.map((image, index) => (
                                            <img 
                                                key={index}
                                                src={`${STATIC_BASE}${image}`}
                                                alt={`Меню ${index + 1}`}
                                                className={`${styles.menuThumbnail} ${activeMenuIndex === index ? styles.activeThumbnail : ''}`}
                                                onClick={() => setActiveMenuIndex(index)}
                                            />
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>
                    )}
                </div>

                {/* Секция бронирования */}
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
                        <div className={styles.formGroup}>
                            <label htmlFor="time">Время</label>
                            <select
                                id="time"
                                value={bookingData.time}
                                onChange={(e) => setBookingData({...bookingData, time: e.target.value, table_id: null})}
                                required
                                className={styles.select}
                                disabled={!availableTimeSlots.length}
                            >
                                <option value="">Выберите время</option>
                                {availableTimeSlots.map(slot => (
                                    <option key={slot.start_time} value={slot.start_time}>
                                        {slot.start_time.substring(0,5)} - {slot.end_time.substring(0,5)}
                                    </option>
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

                {/* Секция отзывов */}
                <ReviewsSection restaurantId={restaurant.id} />
            </div>
            <Footer />
        </>
    );
} 