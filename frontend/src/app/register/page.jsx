"use client";
import { useState } from "react";
import { useAuth } from "@/shared/store";
import api from "@/shared/api";
import { useRouter } from "next/navigation";
import styles from "./register.module.css";

export default function RegisterPage() {
  const { setUser, setToken } = useAuth();
  const router = useRouter();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
    name: ""
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

    if (formData.password !== formData.confirmPassword) {
      setError("Пароли не совпадают");
      return;
    }

    if (formData.password.length < 6) {
      setError("Пароль должен содержать минимум 6 символов");
      return;
    }

    setLoading(true);

    try {
      const response = await api.post("/auth/register", {
        email: formData.email,
        password: formData.password,
        name: formData.name
      });
      
      setToken(response.data.access_token);
      const decoded = JSON.parse(atob(response.data.access_token.split('.')[1]));
      setUser({ 
        id: decoded.sub, 
        email: formData.email, 
        name: formData.name, 
        role: decoded.role 
      });
      router.push("/");
    } catch (error) {
      if (error.response?.data?.detail) {
        setError(error.response.data.detail);
      } else {
        setError("Ошибка при регистрации");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.registerCard}>
        <div className={styles.logo}>
          <span className={styles.logoIcon}>🍽️</span>
          <h1>Регистрация</h1>
        </div>
        
        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.inputGroup}>
            <label htmlFor="name">Имя</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className={styles.input}
              placeholder="Введите ваше имя"
            />
          </div>

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
              placeholder="Введите пароль (минимум 6 символов)"
            />
          </div>

          <div className={styles.inputGroup}>
            <label htmlFor="confirmPassword">Подтвердите пароль</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              className={styles.input}
              placeholder="Повторите пароль"
            />
          </div>
          
          {error && <div className={styles.error}>{error}</div>}
          
          <button 
            type="submit" 
            className={styles.submitButton}
            disabled={loading}
          >
            {loading ? "Регистрация..." : "Зарегистрироваться"}
          </button>
        </form>
        
        <div className={styles.footer}>
          <p>Уже есть аккаунт? <a href="/login" className={styles.link}>Войти</a></p>
        </div>
      </div>
    </div>
  );
} 