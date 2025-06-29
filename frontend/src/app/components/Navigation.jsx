"use client";
import { useAuth } from "../../shared/store";
import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";
import styles from "./Navigation.module.css";

export default function Navigation() {
    const { user, logout } = useAuth();
    const router = useRouter();
    const pathname = usePathname();

    const handleLogout = () => {
        logout();
        router.push("/");
    };

    const isActive = (path) => {
        return pathname === path;
    };

    return (
        <nav className={styles.navbar}>
            <div className={styles.container}>
                <Link href="/" className={styles.logo}>
                    🍽️ Рестораны Владивостока
                </Link>

                <div className={styles.navLinks}>
                    <Link 
                        href="/restaurants" 
                        className={`${styles.navLink} ${isActive('/restaurants') ? styles.active : ''}`}
                    >
                        Рестораны
                    </Link>
                    
                    {user && (
                        <>
                            <Link 
                                href="/bookings" 
                                className={`${styles.navLink} ${isActive('/bookings') ? styles.active : ''}`}
                            >
                                Мои бронирования
                            </Link>
                            
                            {user.role === "admin" && (
                                <Link 
                                    href="/admin" 
                                    className={`${styles.navLink} ${isActive('/admin') ? styles.active : ''}`}
                                >
                                    Админ панель
                                </Link>
                            )}
                        </>
                    )}
                </div>

                <div className={styles.authSection}>
                    {user ? (
                        <div className={styles.userMenu}>
                            <span className={styles.userName}>
                                {user.name} {user.role === "admin" && <span className={styles.adminBadge}>Admin</span>}
                            </span>
                            <button onClick={handleLogout} className={styles.logoutButton}>
                                Выйти
                            </button>
                        </div>
                    ) : (
                        <div className={styles.authButtons}>
                            <Link href="/login" className={styles.loginButton}>
                                Войти
                            </Link>
                            <Link href="/register" className={styles.registerButton}>
                                Регистрация
                            </Link>
                        </div>
                    )}
                </div>
            </div>
        </nav>
    );
} 