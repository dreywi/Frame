from models import Ingredient, Recipe, User
from models.reviews import create_review
from storage import (
    load_recipes,
    load_reviews,
    load_users,
    save_recipes,
    save_reviews,
    save_users,
)


def test_round_trip(tmp_path):
    users = [User(1, "Анна", "anna@example.com")]
    recipes = [Recipe(1, "Омлет", "Завтраки", 1, 10, 320.0,
                      [Ingredient("Яйца", 3, "шт")])]
    reviews = []
    create_review(reviews, recipes[0], users[0], 4, "Вкусно")
    reviews[0].delete()

    save_users(users, tmp_path / "users.json")
    save_recipes(recipes, tmp_path / "recipes.json")
    save_reviews(reviews, tmp_path / "reviews.json")

    loaded_users = load_users(tmp_path / "users.json")
    loaded_recipes = load_recipes(tmp_path / "recipes.json")
    loaded_reviews = load_reviews(loaded_recipes, loaded_users,
                                  tmp_path / "reviews.json")

    assert loaded_users[0].email == "anna@example.com"
    assert loaded_recipes[0].ingredients[0].name == "Яйца"
    assert loaded_reviews[0].recipe is loaded_recipes[0]
    assert loaded_reviews[0].user is loaded_users[0]
    assert loaded_reviews[0].is_deleted


def test_missing_file_returns_empty(tmp_path):
    assert load_users(tmp_path / "nope.json") == []


def test_broken_json_returns_empty(tmp_path):
    path = tmp_path / "users.json"
    path.write_text("{broken", encoding="utf-8")
    assert load_users(path) == []


def test_review_with_unknown_recipe_skipped(tmp_path):
    path = tmp_path / "reviews.json"
    path.write_text(
        '[{"id": 1, "recipe_id": 9, "user_id": 1, "rating": 5}]',
        encoding="utf-8",
    )
    users = [User(1, "Анна", "anna@example.com")]
    assert load_reviews([], users, path) == []
