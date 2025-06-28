"use client";
import { useState, useEffect } from "react";
import { useAuth } from "../shared/store";
import api from "../shared/api";
import { useRouter } from "next/navigation";
import styles from "./page.module.css";

export default function Home() {
  const { user } = useAuth();
  const router = useRouter();
  const [restaurants, setRestaurants] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [cuisineFilter, setCuisineFilter] = useState("");
  const [priceFilter, setPriceFilter] = useState("");
  const [ratingFilter, setRatingFilter] = useState("");

  useEffect(() => {
    fetchRestaurants();
  }, []);

  const fetchRestaurants = async () => {
    try {
      const response = await api.get("/restaurants/");
      setRestaurants(response.data);
    } catch (error) {
      console.error("Error fetching restaurants:", error);
    }
  };

  const filteredRestaurants = restaurants.filter((restaurant) => {
    const matchesSearch = restaurant.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         restaurant.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCuisine = !cuisineFilter || restaurant.cuisine === cuisineFilter;
    const matchesPrice = !priceFilter || restaurant.price_range === priceFilter;
    const matchesRating = !ratingFilter || restaurant.rating >= parseInt(ratingFilter);
    
    return matchesSearch && matchesCuisine && matchesPrice && matchesRating;
  });

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

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <div className={styles.logo}>
            <span className={styles.logoIcon}>🍽️</span>
            <h1>Ресторанный сервис</h1>
          </div>
          <nav className={styles.nav}>
            {user ? (
              <>
                <button 
                  className={styles.navButton}
                  onClick={() => router.push("/bookings")}
                >
                  <span className={styles.navIcon}>📅</span>
                  Мои брони
                </button>
                <button 
                  className={styles.navButton}
                  onClick={() => router.push("/profile")}
                >
                  <span className={styles.navIcon}>👤</span>
                  {user.email}
                </button>
              </>
            ) : (
              <button 
                className={styles.navButton}
                onClick={() => router.push("/login")}
              >
                Войти
              </button>
            )}
          </nav>
        </div>
      </header>

      <main className={styles.main}>
        <div className={styles.hero}>
          <h2 className={styles.heroTitle}>Найдите идеальный ресторан</h2>
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
                value={ratingFilter}
                onChange={(e) => setRatingFilter(e.target.value)}
                className={styles.select}
              >
                <option value="">Любой рейтинг</option>
                <option value="4">4+ звезды</option>
                <option value="3">3+ звезды</option>
                <option value="2">2+ звезды</option>
              </select>
            </div>
          </div>
        </div>

        {/* Список ресторанов */}
        <div className={styles.restaurantsGrid}>
          {filteredRestaurants.map((restaurant) => (
            <div 
              key={restaurant.id} 
              className={styles.restaurantCard}
              onClick={() => router.push(`/restaurants/${restaurant.id}`)}
            >
              <div className={styles.cardImage}>
                <img 
                  src={restaurant.image_url || "https://via.placeholder.com/400x200?text=Ресторан"} 
                  alt={restaurant.name}
                />
              </div>
              <div className={styles.cardContent}>
                <h3 className={styles.restaurantName}>{restaurant.name}</h3>
                <p className={styles.restaurantDescription}>{restaurant.description}</p>
                <div className={styles.rating}>
                  {renderStars(restaurant.rating)}
                  <span className={styles.ratingText}>({restaurant.rating})</span>
                </div>
                <div className={styles.tags}>
                  <span className={styles.tag}>{restaurant.cuisine}</span>
                  <span className={styles.tagOutline}>{restaurant.price_range}</span>
                </div>
                <p className={styles.address}>{restaurant.address}</p>
              </div>
            </div>
          ))}
        </div>

        {filteredRestaurants.length === 0 && (
          <div className={styles.emptyState}>
            <p>Рестораны не найдены</p>
          </div>
        )}
      </main>
    </div>
  );
}
