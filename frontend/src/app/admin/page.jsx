"use client";
import { useAuth } from "../../shared/store";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import styles from "./admin.module.css";

export default function AdminPage() {
    const { user } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!user || user.role !== "admin") {
            router.push("/login");
        }
    }, [user, router]);

    if (!user || user.role !== "admin") {
        return (
            <div className={styles.container}>
                <div className={styles.loading}>Проверка прав доступа...</div>
            </div>
        );
    }

    return (
        <div className={styles.container}>
            <h1 className={styles.title}>Панель администратора</h1>
            <div className={styles.content}>
                <div className={styles.section}>
                    <h2>Управление ресторанами</h2>
                    <p>Здесь будет CRUD ресторанов, столиков, бронирований, загрузка фото</p>
                </div>
            </div>
        </div>
    );
} 