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
            setUser({ 
                id: decoded.sub, 
                email: formData.email, 
                name: "", 
                role: decoded.role 
            });
            router.push("/");
        } catch (error) {
            setError("Неверный email или пароль");
        } finally {
            setLoading(false);
        }
    };

    return (
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
                        <input
                            type="password"
                            id="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            required
                            className={styles.input}
                            placeholder="Введите ваш пароль"
                        />
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
    );
} 