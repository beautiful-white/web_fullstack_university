"use client";
import { useRouter } from "next/navigation";
import { useAuth } from "../shared/store";
import styles from "./page.module.css";
import Footer from "./components/Footer";

export default function HomePage() {
    const router = useRouter();
    const { user } = useAuth();

    return (
        <>
            <div className={styles.background}></div>
            {/* Hero Section на всю ширину */}
            <div className={styles.heroSection}>
                <div className={styles.heroContentWrap}>
                    <div className={styles.heroContent}>
                        <h1 className={styles.title}>
                            Откройте для себя лучшие рестораны Владивостока
                        </h1>
                        <p className={styles.subtitle}>
                            Насладитесь изысканной кухней в уютной атмосфере. Бронируйте столики в любимых ресторанах города с комфортом.
                        </p>
                        <div className={styles.heroButtons}>
                            <button 
                                className={styles.primaryButton}
                                onClick={() => router.push("/restaurants")}
                            >
                                Выбрать ресторан
                            </button>
                            {!user && (
                                <button 
                                    className={styles.secondaryButton}
                                    onClick={() => router.push("/register")}
                                >
                                    Присоединиться
                                </button>
                            )}
                        </div>
                    </div>
                    <div className={styles.heroImage}>
                        <div className={styles.imagePlaceholder}>
                            <img 
                                src="/fork-and-spoon-meal-svgrepo.svg" 
                                alt="Вилка и ложка"
                            />
                        </div>
                    </div>
                </div>
            </div>
            {/* Features Section на всю ширину */}
            <div className={styles.featuresSection}>
                <div className={styles.featuresContentWrap}>
                    <h2 className={styles.featuresTitle}>Что мы предлагаем</h2>
                    <div className={styles.featuresGrid}>
                        <div className={styles.feature}>
                            <div className={styles.featureIcon}>🔍</div>
                            <h3>Широкий выбор</h3>
                            <p>Множество ресторанов с различными кухнями мира - от традиционной русской до экзотической азиатской</p>
                        </div>
                        <div className={styles.feature}>
                            <div className={styles.featureIcon}>📅</div>
                            <h3>Простое бронирование</h3>
                            <p>Забронируйте столик в несколько кликов. Выбирайте удобное время и количество гостей</p>
                        </div>
                        <div className={styles.feature}>
                            <div className={styles.featureIcon}>⭐</div>
                            <h3>Честные отзывы</h3>
                            <p>Реальные отзывы посетителей помогут сделать правильный выбор ресторана</p>
                        </div>
                        <div className={styles.feature}>
                            <div className={styles.featureIcon}>🎯</div>
                            <h3>Персональные рекомендации</h3>
                            <p>Получайте предложения на основе ваших предпочтений и истории посещений</p>
                        </div>
                    </div>
                </div>
            </div>
            {/* CTA Section на всю ширину */}
            {!user && (
                <div className={styles.ctaSection}>
                    <div className={styles.ctaContentWrap}>
                        <h2>Начните прямо сейчас</h2>
                        <p>Создайте аккаунт и получите доступ к эксклюзивным предложениям и скидкам</p>
                        <button 
                            className={styles.ctaButton}
                            onClick={() => router.push("/register")}
                        >
                            Зарегистрироваться
                        </button>
                    </div>
                </div>
            )}
            {/* About Section на всю ширину */}
            <div className={styles.about}>
                <div className={styles.aboutContent}>
                    <h2>О нашем сервисе</h2>
                    <p>
                        Мы создали платформу, которая объединяет лучшие рестораны Владивостока в одном месте. 
                        Наша миссия - помочь вам найти идеальное место для любого случая: романтического ужина, 
                        деловой встречи или семейного праздника.
                    </p>
                    <p>
                        Каждый ресторан в нашей базе проходит тщательную проверку, чтобы гарантировать 
                        высокое качество обслуживания и кухни. Мы сотрудничаем только с проверенными заведениями, 
                        которые ценят своих гостей.
                    </p>
                </div>
            </div>
            {/* Footer на всю ширину */}
            <Footer />
        </>
    );
}
