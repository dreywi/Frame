"""Загрузка и сохранение данных в JSON."""

import json
from pathlib import Path
from typing import List

from models import Ingredient, Recipe, Review, User
from models.recipes import find_recipe_by_id
from models.users import find_user_by_id

DATA_DIR = Path(__file__).parent / "data"
USERS_FILE = DATA_DIR / "users.json"
RECIPES_FILE = DATA_DIR / "recipes.json"
REVIEWS_FILE = DATA_DIR / "reviews.json"


def _read_json(path: Path) -> list:
    """Прочитать список из JSON-файла. При ошибке вернуть пустой список."""
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл не найден: {path}, начинаем с пустого списка")
        return []
    except json.JSONDecodeError as error:
        print(f"Ошибка формата JSON в {path}: {error}")
        return []


def _write_json(path: Path, data: list) -> None:
    """Записать список в JSON-файл."""
    path.parent.mkdir(exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_users(path: Path = USERS_FILE) -> List[User]:
    """Загрузить пользователей и создать объекты User."""
    users = []
    for data in _read_json(path):
        try:
            users.append(User.from_data(data))
        except (KeyError, ValueError) as error:
            print(f"Пропущен пользователь {data}: {error}")
    return users


def save_users(users: List[User], path: Path = USERS_FILE) -> None:
    """Сохранить объекты User в JSON."""
    data = [
        {"id": user.id, "name": user.name, "email": user.email}
        for user in users
    ]
    _write_json(path, data)


def _recipe_from_data(data: dict) -> Recipe:
    """Создать объект Recipe с ингредиентами из данных JSON."""
    ingredients = [
        Ingredient(item["name"], item["amount"], item["unit"])
        for item in data.get("ingredients", [])
    ]
    return Recipe(
        data["id"],
        data["title"],
        data["category"],
        data["servings"],
        data["cook_time_min"],
        data["calories_per_serving"],
        ingredients,
    )


def load_recipes(path: Path = RECIPES_FILE) -> List[Recipe]:
    """Загрузить рецепты и создать объекты Recipe."""
    recipes = []
    for data in _read_json(path):
        try:
            recipes.append(_recipe_from_data(data))
        except (KeyError, ValueError) as error:
            print(f"Пропущен рецепт {data.get('id')}: {error}")
    return recipes


def save_recipes(recipes: List[Recipe], path: Path = RECIPES_FILE) -> None:
    """Сохранить объекты Recipe в JSON."""
    data = [
        {
            "id": recipe.id,
            "title": recipe.title,
            "category": recipe.category,
            "servings": recipe.servings,
            "cook_time_min": recipe.cook_time_min,
            "calories_per_serving": recipe.calories_per_serving,
            "ingredients": [
                {"name": item.name, "amount": item.amount, "unit": item.unit}
                for item in recipe.ingredients
            ],
        }
        for recipe in recipes
    ]
    _write_json(path, data)


def load_reviews(
    recipes: List[Recipe],
    users: List[User],
    path: Path = REVIEWS_FILE,
) -> List[Review]:
    """Загрузить отзывы, восстановив связи с Recipe и User."""
    reviews = []
    for data in _read_json(path):
        try:
            recipe = find_recipe_by_id(recipes, data["recipe_id"])
            user = find_user_by_id(users, data["user_id"])
            if recipe is None or user is None:
                print(f"Пропущен отзыв {data['id']}: "
                      "не найден рецепт или пользователь")
                continue
            review = Review(data["id"], recipe, user, data["rating"],
                            data.get("comment", ""))
            review.is_deleted = data.get("is_deleted", False)
            reviews.append(review)
        except (KeyError, ValueError) as error:
            print(f"Пропущен отзыв {data.get('id')}: {error}")
    return reviews


def save_reviews(reviews: List[Review], path: Path = REVIEWS_FILE) -> None:
    """Сохранить отзывы, заменив ссылки на объекты идентификаторами."""
    data = [
        {
            "id": review.id,
            "recipe_id": review.recipe.id,
            "user_id": review.user.id,
            "rating": review.rating,
            "comment": review.comment,
            "is_deleted": review.is_deleted,
        }
        for review in reviews
    ]
    _write_json(path, data)
