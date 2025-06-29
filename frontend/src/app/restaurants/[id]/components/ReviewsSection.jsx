"use client";
import { useState, useEffect } from "react";
import { useAuth } from "@/shared/store";
import api from "@/shared/api";
import styles from "./ReviewsSection.module.css";

export default function ReviewsSection({ restaurantId }) {
    const { user } = useAuth();
    const [reviews, setReviews] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showForm, setShowForm] = useState(false);
    const [formData, setFormData] = useState({
        rating: 5,
        comment: ""
    });
    const [submitting, setSubmitting] = useState(false);
    const [userReview, setUserReview] = useState(null);

    useEffect(() => {
        fetchReviews();
    }, [restaurantId]);

    const fetchReviews = async () => {
        try {
            const response = await api.get(`/reviews/restaurant/${restaurantId}`);
            setReviews(response.data);

            // Проверяем, есть ли отзыв от текущего пользователя
            if (user) {
                const userReview = response.data.find(review => review.user_id === user.id);
                setUserReview(userReview);
            }
        } catch (error) {
            console.error("Error fetching reviews:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitting(true);

        try {
            await api.post("/reviews/", {
                restaurant_id: restaurantId,
                rating: formData.rating,
                comment: formData.comment
            });

            setFormData({ rating: 5, comment: "" });
            setShowForm(false);
            fetchReviews();
            alert("Отзыв успешно добавлен!");
        } catch (error) {
            if (error.response?.data?.detail) {
                alert(error.response.data.detail);
            } else {
                alert("Ошибка при добавлении отзыва");
            }
        } finally {
            setSubmitting(false);
        }
    };

    const handleUpdateReview = async (e) => {
        e.preventDefault();
        setSubmitting(true);

        try {
            await api.put(`/reviews/${userReview.id}`, {
                rating: formData.rating,
                comment: formData.comment
            });

            setFormData({ rating: 5, comment: "" });
            setShowForm(false);
            fetchReviews();
            alert("Отзыв успешно обновлен!");
        } catch (error) {
            if (error.response?.data?.detail) {
                alert(error.response.data.detail);
            } else {
                alert("Ошибка при обновлении отзыва");
            }
        } finally {
            setSubmitting(false);
        }
    };

    const handleDeleteReview = async () => {
        if (!confirm("Вы уверены, что хотите удалить свой отзыв?")) {
            return;
        }

        try {
            await api.delete(`/reviews/${userReview.id}`);
            setUserReview(null);
            fetchReviews();
            alert("Отзыв успешно удален!");
        } catch (error) {
            alert("Ошибка при удалении отзыва");
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

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString("ru-RU");
    };

    if (loading) {
        return (
            <div className={styles.container}>
                <div className={styles.loading}>Загрузка отзывов...</div>
            </div>
        );
    }

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h2 className={styles.title}>Отзывы ({reviews.length})</h2>
                {user && !userReview && (
                    <button
                        className={styles.addReviewButton}
                        onClick={() => setShowForm(true)}
                    >
                        Оставить отзыв
                    </button>
                )}
            </div>

            {/* Форма отзыва */}
            {showForm && (
                <div className={styles.reviewForm}>
                    <h3 className={styles.formTitle}>
                        {userReview ? "Редактировать отзыв" : "Оставить отзыв"}
                    </h3>
                    <form onSubmit={userReview ? handleUpdateReview : handleSubmit}>
                        <div className={styles.ratingSection}>
                            <label className={styles.ratingLabel}>Оценка:</label>
                            <div className={styles.starSelector}>
                                {[1, 2, 3, 4, 5].map(star => (
                                    <button
                                        key={star}
                                        type="button"
                                        className={`${styles.starButton} ${formData.rating >= star ? styles.starSelected : ''}`}
                                        onClick={() => setFormData({...formData, rating: star})}
                                    >
                                        ★
                                    </button>
                                ))}
                            </div>
                        </div>

                        <div className={styles.commentSection}>
                            <label htmlFor="comment" className={styles.commentLabel}>
                                Комментарий:
                            </label>
                            <textarea
                                id="comment"
                                value={formData.comment}
                                onChange={(e) => setFormData({...formData, comment: e.target.value})}
                                className={styles.commentInput}
                                placeholder="Поделитесь своими впечатлениями..."
                                rows="4"
                            />
                        </div>

                        <div className={styles.formActions}>
                            <button
                                type="button"
                                className={styles.cancelButton}
                                onClick={() => {
                                    setShowForm(false);
                                    setFormData({ rating: 5, comment: "" });
                                }}
                            >
                                Отмена
                            </button>
                            <button
                                type="submit"
                                className={styles.submitButton}
                                disabled={submitting}
                            >
                                {submitting ? "Сохранение..." : (userReview ? "Обновить" : "Отправить")}
                            </button>
                        </div>
                    </form>
                </div>
            )}

            {/* Отзыв пользователя */}
            {userReview && !showForm && (
                <div className={styles.userReview}>
                    <div className={styles.userReviewHeader}>
                        <h3>Ваш отзыв</h3>
                        <div className={styles.userReviewActions}>
                            <button
                                className={styles.editButton}
                                onClick={() => {
                                    setFormData({ rating: userReview.rating, comment: userReview.comment || "" });
                                    setShowForm(true);
                                }}
                            >
                                Редактировать
                            </button>
                            <button
                                className={styles.deleteButton}
                                onClick={handleDeleteReview}
                            >
                                Удалить
                            </button>
                        </div>
                    </div>
                    <div className={styles.reviewContent}>
                        <div className={styles.reviewRating}>
                            {renderStars(userReview.rating)}
                        </div>
                        {userReview.comment && (
                            <p className={styles.reviewComment}>{userReview.comment}</p>
                        )}
                        <div className={styles.reviewDate}>
                            {formatDate(userReview.created_at)}
                        </div>
                    </div>
                </div>
            )}

            {/* Список отзывов */}
            <div className={styles.reviewsList}>
                {reviews.length === 0 ? (
                    <div className={styles.noReviews}>
                        Пока нет отзывов. Будьте первым!
                    </div>
                ) : (
                    reviews.map((review) => (
                        <div key={review.id} className={styles.reviewCard}>
                            <div className={styles.reviewHeader}>
                                <div className={styles.reviewAuthor}>
                                    {review.user_name || "Пользователь"}
                                </div>
                                <div className={styles.reviewRating}>
                                    {renderStars(review.rating)}
                                </div>
                            </div>
                            {review.comment && (
                                <p className={styles.reviewComment}>{review.comment}</p>
                            )}
                            <div className={styles.reviewDate}>
                                {formatDate(review.created_at)}
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}