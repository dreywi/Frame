"""Отзывы пользователей на рецепты."""

from typing import List, Optional

from .recipes import Recipe
from .users import User


class Review:
    """Отзыв пользователя на рецепт."""

    def __init__(
        self,
        review_id: int,
        recipe: Recipe,
        user: User,
        rating: int,
        comment: str = "",
    ) -> None:
        if not 1 <= rating <= 5:
            raise ValueError(f"Оценка должна быть от 1 до 5: {rating}")
        self.id = review_id
        self.recipe = recipe
        self.user = user
        self.rating = rating
        self.comment = comment
        self.is_deleted = False

    def delete(self) -> None:
        """Пометить отзыв как удаленный."""
        self.is_deleted = True

    def __str__(self) -> str:
        state = "удален" if self.is_deleted else "активен"
        text = f"[{self.id}] {self.recipe.title} - {self.user.name}: "
        text += f"{self.rating}/5 ({state})"
        if self.comment:
            text += f" \"{self.comment}\""
        return text


def can_review(reviews: List[Review], recipe: Recipe, user: User) -> bool:
    """Проверить, нет ли у пользователя активного отзыва на рецепт."""
    for review in reviews:
        if (review.recipe.id == recipe.id and review.user.id == user.id
                and not review.is_deleted):
            return False
    return True


def create_review(
    reviews: List[Review],
    recipe: Recipe,
    user: User,
    rating: int,
    comment: str = "",
) -> Optional[Review]:
    """Создать отзыв, если у пользователя нет активного отзыва на рецепт."""
    if not can_review(reviews, recipe, user):
        return None
    new_id = max((review.id for review in reviews), default=0) + 1
    review = Review(new_id, recipe, user, rating, comment)
    reviews.append(review)
    return review


def find_review_by_id(reviews: List[Review],
                      review_id: int) -> Optional[Review]:
    """Найти отзыв по идентификатору."""
    for review in reviews:
        if review.id == review_id:
            return review
    return None


def delete_review(reviews: List[Review], review_id: int) -> bool:
    """Удалить активный отзыв. Объект остается в коллекции."""
    review = find_review_by_id(reviews, review_id)
    if review is None or review.is_deleted:
        return False
    review.delete()
    return True


def get_review_status(reviews: List[Review], recipe: Recipe,
                      user: User) -> str:
    """Сообщение о возможности оставить отзыв."""
    if can_review(reviews, recipe, user):
        return "Можно оставить отзыв"
    return "У пользователя уже есть активный отзыв на этот рецепт"


def average_rating(reviews: List[Review], recipe: Recipe) -> Optional[float]:
    """Средняя оценка рецепта по активным отзывам."""
    ratings = [
        review.rating for review in reviews
        if review.recipe.id == recipe.id and not review.is_deleted
    ]
    if not ratings:
        return None
    return round(sum(ratings) / len(ratings), 1)


def show_reviews(reviews: List[Review]) -> None:
    """Вывести список отзывов."""
    if not reviews:
        print("Отзывов нет")
        return
    for review in reviews:
        print(review)
