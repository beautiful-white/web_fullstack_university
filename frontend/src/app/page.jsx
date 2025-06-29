"use client";
import { useRouter } from "next/navigation";
import { useAuth } from "../shared/store";
import styles from "./page.module.css";

export default function HomePage() {
    const router = useRouter();
    const { user } = useAuth();

    return (
        <div className={styles.container}>
            <div className={styles.hero}>
                <div className={styles.heroContent}>
                    <h1 className={styles.title}>
                        Добро пожаловать в мир изысканной кухни
                    </h1>
                    <p className={styles.subtitle}>
                        Откройте для себя лучшие рестораны Владивостока и забронируйте столик в один клик
                    </p>
                    <div className={styles.heroButtons}>
                        <button 
                            className={styles.primaryButton}
                            onClick={() => router.push("/restaurants")}
                        >
                            Найти ресторан
                        </button>
                        {!user && (
                            <button 
                                className={styles.secondaryButton}
                                onClick={() => router.push("/register")}
                            >
                                Зарегистрироваться
                            </button>
                        )}
                    </div>
                </div>
                <div className={styles.heroImage}>
                    <div className={styles.imagePlaceholder}>
                        🍽️
                    </div>
                </div>
            </div>

            <div className={styles.features}>
                <h2 className={styles.featuresTitle}>Почему выбирают нас?</h2>
                <div className={styles.featuresGrid}>
                    <div className={styles.feature}>
                        <div className={styles.featureIcon}>🔍</div>
                        <h3>Удобный поиск</h3>
                        <p>Найдите ресторан по кухне, цене и рейтингу</p>
                    </div>
                    <div className={styles.feature}>
                        <div className={styles.featureIcon}>📅</div>
                        <h3>Быстрое бронирование</h3>
                        <p>Забронируйте столик за несколько секунд</p>
                    </div>
                    <div className={styles.feature}>
                        <div className={styles.featureIcon}>⭐</div>
                        <h3>Отзывы и рейтинги</h3>
                        <p>Читайте отзывы и выбирайте лучшие места</p>
                    </div>
                    <div className={styles.feature}>
                        <div className={styles.featureIcon}>📱</div>
                        <h3>Мобильная версия</h3>
                        <p>Удобно использовать на любом устройстве</p>
                    </div>
                </div>
            </div>

            {!user && (
                <div className={styles.cta}>
                    <h2>Готовы начать?</h2>
                    <p>Зарегистрируйтесь и получите доступ ко всем возможностям</p>
                    <button 
                        className={styles.ctaButton}
                        onClick={() => router.push("/register")}
                    >
                        Создать аккаунт
                    </button>
                </div>
            )}

            {/* Footer */}
            <div className={styles.footer}>
                <div className={styles.footerContent}>
                    <div className={styles.footerSection}>
                        <h3>О нас</h3>
                        <p>Мы помогаем жителям и гостям Владивостока находить лучшие рестораны города</p>
                    </div>
                    <div className={styles.footerSection}>
                        <h3>Навигация</h3>
                        <ul>
                            <li><button onClick={() => router.push("/restaurants")}>Рестораны</button></li>
                            {user && <li><button onClick={() => router.push("/bookings")}>Мои брони</button></li>}
                            {!user && <li><button onClick={() => router.push("/login")}>Войти</button></li>}
                        </ul>
                    </div>
                    <div className={styles.footerSection}>
                        <h3>Контакты</h3>
                        <p>📧 info@vladivostok-restaurants.ru</p>
                        <p>📞 +7 (423) 123-45-67</p>
                    </div>
                </div>
                <div className={styles.footerBottom}>
                    <p>&copy; 2024 Рестораны Владивостока. Все права защищены.</p>
                </div>
            </div>
        </div>
    );
}
