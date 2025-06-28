"use client";
import { useEffect, useState } from "react";
import api from "../../shared/api";
import { useRouter } from "next/navigation";
import styles from "./restaurants.module.css";

export default function RestaurantsPage() {
    const [restaurants, setRestaurants] = useState([]);
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        fetchRestaurants();
    }, []);

    const fetchRestaurants = async () => {
        try {
            const response = await api.get("/restaurants");
            setRestaurants(response.data);
        } catch (error) {
            console.error("Error fetching restaurants:", error);
        } finally {
            setLoading(false);
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
                <div className={styles.loading}>Загрузка ресторанов...</div>
            </div>
        );
    }

    return (
        <div className={styles.container}>
            <h1 className={styles.title}>Все рестораны</h1>
            <div className={styles.grid}>
                {restaurants.map(restaurant => (
                    <div key={restaurant.id} className={styles.card}>
                        <div className={styles.cardImage}>
                            <img 
                                src={restaurant.image_url || "https://via.placeholder.com/300x200?text=Ресторан"} 
                                alt={restaurant.name}
                            />
                        </div>
                        <div className={styles.cardContent}>
                            <h3 className={styles.restaurantName}>{restaurant.name}</h3>
                            <p className={styles.location}>{restaurant.address}</p>
                            <p className={styles.cuisine}>{restaurant.cuisine}</p>
                            <div className={styles.rating}>
                                {renderStars(restaurant.rating)}
                                <span className={styles.ratingText}>({restaurant.rating})</span>
                            </div>
                            <button 
                                className={styles.button}
                                onClick={() => router.push(`/restaurants/${restaurant.id}`)}
                            >
                                Подробнее
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
} 