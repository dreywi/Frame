import pytest

from models import Recipe, Review, User
from models.reviews import (
    average_rating,
    can_review,
    create_review,
    delete_review,
)


@pytest.fixture
def recipe():
    return Recipe(1, "Паста карбонара", "Основные блюда", 2, 25, 640.5)


@pytest.fixture
def user():
    return User(1, "Анна", "anna@example.com")


@pytest.fixture
def another_user():
    return User(2, "Иван", "ivan@example.com")


def test_review_creation(recipe, user):
    review = Review(1, recipe, user, 5, "Отлично")
    assert review.recipe is recipe
    assert review.user is user
    assert review.rating == 5
    assert not review.is_deleted


def test_review_invalid_rating(recipe, user):
    with pytest.raises(ValueError):
        Review(1, recipe, user, 6)


def test_review_delete(recipe, user):
    review = Review(1, recipe, user, 5)
    review.delete()
    assert review.is_deleted
    assert "удален" in str(review)


def test_second_active_review_blocked(recipe, user):
    reviews = []
    assert create_review(reviews, recipe, user, 5) is not None
    assert not can_review(reviews, recipe, user)
    assert create_review(reviews, recipe, user, 4) is None
    assert len(reviews) == 1


def test_deleted_review_does_not_block(recipe, user):
    reviews = []
    first = create_review(reviews, recipe, user, 5)
    assert delete_review(reviews, first.id)
    second = create_review(reviews, recipe, user, 4)
    assert second is not None
    assert len(reviews) == 2


def test_other_user_can_review(recipe, user, another_user):
    reviews = []
    create_review(reviews, recipe, user, 5)
    assert create_review(reviews, recipe, another_user, 3) is not None


def test_delete_review_missing_or_twice(recipe, user):
    reviews = []
    review = create_review(reviews, recipe, user, 5)
    assert not delete_review(reviews, 99)
    assert delete_review(reviews, review.id)
    assert not delete_review(reviews, review.id)


def test_average_rating_ignores_deleted(recipe, user, another_user):
    reviews = []
    create_review(reviews, recipe, user, 5)
    bad = create_review(reviews, recipe, another_user, 1)
    bad.delete()
    assert average_rating(reviews, recipe) == 5.0


def test_average_rating_none(recipe):
    assert average_rating([], recipe) is None
