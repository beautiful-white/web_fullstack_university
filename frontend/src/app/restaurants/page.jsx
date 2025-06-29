"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import api from "../../shared/api";
import styles from "./restaurants.module.css";

function haversine(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const toRad = (x) => (x * Math.PI) / 180;
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
}

// Функция для форматирования расстояния
function formatDistance(distance) {
    if (distance < 1) {
        return `${(distance * 1000).toFixed(0)} м`;
    } else if (distance < 10) {
        return `${distance.toFixed(1)} км`;
    } else {
        return `${distance.toFixed(0)} км`;
    }
}

export default function RestaurantsPage() {
    const [restaurants, setRestaurants] = useState([]);
    const [loading, setLoading] = useState(true);
    const [locationLoading, setLocationLoading] = useState(false);
    const [searchTerm, setSearchTerm] = useState("");
    const [cuisineFilter, setCuisineFilter] = useState("");
    const [priceFilter, setPriceFilter] = useState("");
    const [minRating, setMinRating] = useState("");
    const [useLocation, setUseLocation] = useState(false);
    const [userCoords, setUserCoords] = useState(null);
    const [locationError, setLocationError] = useState("");
    const router = useRouter();

    useEffect(() => {
        if (useLocation && userCoords) {
            fetchRestaurants(userCoords);
        } else {
            fetchRestaurants();
        }
    }, [cuisineFilter, priceFilter, minRating, useLocation, userCoords]);

    const fetchRestaurants = async (coords) => {
        try {
            setLoading(true);
            const params = {};
            if (cuisineFilter) params.cuisine = cuisineFilter;
            if (priceFilter) params.price_range = priceFilter;
            if (minRating) params.min_rating = parseFloat(minRating);
            if (coords) {
                params.lat = coords.latitude;
                params.lon = coords.longitude;
            }
            const response = await api.get("/restaurants/", { params });
            setRestaurants(response.data);
        } catch (error) {
            console.error("Error fetching restaurants:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleFindNearest = () => {
        if (!navigator.geolocation) {
            setLocationError("Геолокация не поддерживается вашим браузером");
            return;
        }
        
        setLocationLoading(true);
        setLocationError("");
        
        navigator.geolocation.getCurrentPosition(
            (position) => {
                setUserCoords({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                });
                setUseLocation(true);
                setLocationLoading(false);
            },
            (error) => {
                let errorMessage = "Не удалось получить геолокацию";
                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        errorMessage = "Доступ к геолокации запрещен. Разрешите доступ в настройках браузера.";
                        break;
                    case error.POSITION_UNAVAILABLE:
                        errorMessage = "Информация о местоположении недоступна";
                        break;
                    case error.TIMEOUT:
                        errorMessage = "Превышено время ожидания получения геолокации";
                        break;
                    default:
                        errorMessage = "Произошла ошибка при получении геолокации";
                }
                setLocationError(errorMessage);
                setLocationLoading(false);
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 60000
            }
        );
    };

    const handleResetLocation = () => {
        setUseLocation(false);
        setUserCoords(null);
        setLocationError("");
        setLoading(true);
        fetchRestaurants();
    };

    const handleResetFilters = () => {
        setSearchTerm("");
        setCuisineFilter("");
        setPriceFilter("");
        setMinRating("");
        setUseLocation(false);
        setUserCoords(null);
        setLocationError("");
        setLoading(true);
        fetchRestaurants();
    };

    // Фильтрация по поиску и радиусу
    let filteredRestaurants = restaurants.filter(restaurant =>
        restaurant.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        restaurant.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        restaurant.cuisine.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (useLocation && userCoords) {
        filteredRestaurants = filteredRestaurants
            .map(r => {
                if (r.latitude && r.longitude) {
                    const distance = haversine(userCoords.latitude, userCoords.longitude, r.latitude, r.longitude);
                    return { ...r, distance };
                }
                return { ...r, distance: null };
            })
            .filter(r => r.distance !== null)
            .sort((a, b) => a.distance - b.distance);
    } else {
        const vladivostokCoords = { latitude: 43.1198, longitude: 131.8869 };
        filteredRestaurants = filteredRestaurants
            .map(r => {
                if (r.latitude && r.longitude) {
                    const distance = haversine(vladivostokCoords.latitude, vladivostokCoords.longitude, r.latitude, r.longitude);
                    return { ...r, distance };
                }
                return { ...r, distance: null };
            })
            .filter(r => r.distance !== null)
            .sort((a, b) => a.distance - b.distance);
    }

    const cuisines = [...new Set(restaurants.map(r => r.cuisine))];
    const priceRanges = [...new Set(restaurants.map(r => r.price_range))];

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
            <>
                <div className={styles.background}></div>
                <div className={styles.container}>
                    <div className={styles.loading}>Загрузка ресторанов...</div>
                </div>
            </>
        );
    }

    return (
        <>
            <div className={styles.background}></div>
            <div className={styles.container}>
                <div className={styles.header}>
                    <h1 className={styles.title}>Рестораны Владивостока</h1>
                    <p className={styles.subtitle}>Найдите идеальное место для ужина</p>
                </div>

                {/* Фильтры */}
                <div className={styles.filters}>
                    <div className={styles.filterGrid}>
                        <div className={styles.filterItem}>
                            <input
                                type="text"
                                placeholder="Поиск ресторанов..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className={styles.searchInput}
                            />
                        </div>
                        <div className={styles.filterItem}>
                            <select
                                value={cuisineFilter}
                                onChange={(e) => setCuisineFilter(e.target.value)}
                                className={styles.select}
                            >
                                <option value="">Все кухни</option>
                                {cuisines.map((cuisine) => (
                                    <option key={cuisine} value={cuisine}>
                                        {cuisine}
                                    </option>
                                ))}
                            </select>
                        </div>
                        <div className={styles.filterItem}>
                            <select
                                value={priceFilter}
                                onChange={(e) => setPriceFilter(e.target.value)}
                                className={styles.select}
                            >
                                <option value="">Любая цена</option>
                                {priceRanges.map((price) => (
                                    <option key={price} value={price}>
                                        {price}
                                    </option>
                                ))}
                            </select>
                        </div>
                        <div className={styles.filterItem}>
                            <select
                                value={minRating}
                                onChange={(e) => setMinRating(e.target.value)}
                                className={styles.select}
                            >
                                <option value="">Любой рейтинг</option>
                                <option value="4.5">4.5+ звезд</option>
                                <option value="4.0">4.0+ звезд</option>
                                <option value="3.5">3.5+ звезд</option>
                            </select>
                        </div>
                        <div className={styles.filterItem}>
                            {!useLocation ? (
                                <div className={styles.locationControls}>
                                    <button 
                                        className={`${styles.nearestButton} ${locationLoading ? styles.loadingButton : ''}`} 
                                        onClick={handleFindNearest}
                                        disabled={locationLoading}
                                    >
                                        {locationLoading ? 'Получение геолокации...' : 'Показать ближайшие'}
                                    </button>
                                </div>
                            ) : (
                                <div className={styles.locationControls}>
                                    <button className={styles.resetButton} onClick={handleResetLocation}>
                                        Сбросить геолокацию
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                    
                    {/* Сообщение об ошибке геолокации */}
                    {locationError && (
                        <div className={styles.errorMessage}>
                            <span className={styles.errorIcon}>⚠️</span>
                            {locationError}
                        </div>
                    )}
                    
                    {/* Кнопка сброса фильтров */}
                    <div className={styles.resetFiltersContainer}>
                        <button 
                            className={styles.resetFiltersButton}
                            onClick={handleResetFilters}
                        >
                            <span>🔄</span>
                            Сбросить все фильтры
                        </button>
                    </div>
                </div>

                {/* Список ресторанов */}
                <div className={styles.restaurantsGrid}>
                    {filteredRestaurants.length === 0 ? (
                        <div className={styles.noResults}>
                            <div className={styles.noResultsIcon}>🍽️</div>
                            <h2>Рестораны не найдены</h2>
                            <p>Попробуйте изменить параметры поиска</p>
                            {useLocation && (
                                <p className={styles.noResultsHint}>
                                    Попробуйте увеличить радиус поиска или сбросить геолокацию
                                </p>
                            )}
                        </div>
                    ) : (
                        filteredRestaurants.map((restaurant) => (
                            <div 
                                key={restaurant.id} 
                                className={styles.restaurantCard}
                                onClick={() => router.push(`/restaurants/${restaurant.id}`)}
                            >
                                <div className={styles.imageContainer}>
                                    <img
                                        src={restaurant.image_url || "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80"}
                                        alt={restaurant.name}
                                        className={styles.restaurantImage}
                                    />
                                    <div className={styles.ratingBadge}>
                                        {renderStars(restaurant.rating)}
                                        <span className={styles.ratingNumber}>{restaurant.rating}</span>
                                    </div>
                                    <div className={styles.priceBadge}>
                                        {restaurant.price_range}
                                    </div>
                                    {useLocation && restaurant.distance !== undefined && (
                                        <div className={styles.distanceBadge}>
                                            📍 {formatDistance(restaurant.distance)}
                                        </div>
                                    )}
                                </div>
                                
                                <div className={styles.restaurantInfo}>
                                    <h3 className={styles.restaurantName}>{restaurant.name}</h3>
                                    <p className={styles.cuisine}>{restaurant.cuisine}</p>
                                    <p className={styles.description}>
                                        {restaurant.description?.length > 100 
                                            ? restaurant.description.substring(0, 100) + '...' 
                                            : restaurant.description}
                                    </p>
                                    <div className={styles.location}>
                                        📍 {restaurant.location}
                                    </div>
                                    {useLocation && restaurant.distance !== undefined && (
                                        <div className={styles.distance}>
                                            🚶 {formatDistance(restaurant.distance)}
                                        </div>
                                    )}
                                    <div className={styles.cardActions}>
                                        <button className={styles.viewButton}>
                                            Подробнее
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ))
                    )}
                </div>

                {filteredRestaurants.length > 0 && (
                    <div className={styles.resultsInfo}>
                        Найдено ресторанов: {filteredRestaurants.length}
                        {useLocation && (
                            <span className={styles.resultsLocation}>
                                • Сортировка: от ближайших
                            </span>
                        )}
                    </div>
                )}
            </div>
        </>
    );
} 