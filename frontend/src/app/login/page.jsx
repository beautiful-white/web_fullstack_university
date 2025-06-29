"use client";
import { useState } from "react";
import { useAuth } from "../../shared/store";
import api from "../../shared/api";
import { useRouter } from "next/navigation";
import styles from "./login.module.css";

export default function LoginPage() {
    const { setUser, setToken } = useAuth();
    const router = useRouter();
    const [formData, setFormData] = useState({
        email: "",
        password: ""
    });
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setLoading(true);
        try {
            const response = await api.post("/auth/login", {
                username: formData.email,
                password: formData.password,
            });
            setToken(response.data.access_token);
            const decoded = JSON.parse(atob(response.data.access_token.split('.')[1]));
            let role = (decoded.role === "admin" || decoded.role === "UserRole.admin") ? "admin" : decoded.role;
            setUser({ 
                id: decoded.sub, 
                email: formData.email, 
                name: "", 
                role
            });
            if (role === "admin") {
                router.push("/admin");
            } else {
                router.push("/");
            }
        } catch (error) {
            setError("Неверный email или пароль");
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <div className={styles.background}></div>
            <div className={styles.container}>
                <div className={styles.loginCard}>
                    <div className={styles.logo}>
                        <span className={styles.logoIcon}>🍽️</span>
                        <h1>Вход в систему</h1>
                    </div>
                    <form onSubmit={handleSubmit} className={styles.form}>
                        <div className={styles.inputGroup}>
                            <label htmlFor="email">Email</label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                required
                                className={styles.input}
                                placeholder="Введите ваш email"
                            />
                        </div>
                        <div className={styles.inputGroup}>
                            <label htmlFor="password">Пароль</label>
                            <div className={styles.inputIconWrapper}>
                              <input
                                  type={showPassword ? "text" : "password"}
                                  id="password"
                                  name="password"
                                  value={formData.password}
                                  onChange={handleChange}
                                  required
                                  className={styles.input}
                                  placeholder="Введите ваш пароль"
                              />
                              <button
                                type="button"
                                onClick={() => setShowPassword((v) => !v)}
                                className={styles.iconButton}
                                title={showPassword ? 'Скрыть пароль' : 'Показать пароль'}
                              >
                                {showPassword ? (
                                  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
                                  </svg>
                                ) : (
                                  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z"/>
                                  </svg>
                                )}
                              </button>
                            </div>
                        </div>
                        {error && <div className={styles.error}>{error}</div>}
                        <button 
                            type="submit" 
                            className={styles.submitButton}
                            disabled={loading}
                        >
                            {loading ? "Вход..." : "Войти"}
                        </button>
                    </form>
                    <div className={styles.footer}>
                        <p>Нет аккаунта? <a href="/register" className={styles.link}>Зарегистрироваться</a></p>
                    </div>
                </div>
            </div>
        </>
    );
} 