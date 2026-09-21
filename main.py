"""Сервис рецептов: консольное приложение."""

from typing import List

from models import Recipe, Review, User
from models.recipes import (
    add_recipe,
    filter_recipes_by_time,
    find_recipe,
    find_recipe_by_id,
    show_recipe_card,
    show_recipes,
    sort_recipes,
)
from models.reviews import (
    average_rating,
    create_review,
    delete_review,
    get_review_status,
    show_reviews,
)
from models.users import add_user, find_user_by_id, show_users
from storage import (
    load_recipes,
    load_reviews,
    load_users,
    save_recipes,
    save_reviews,
    save_users,
)
from utils import input_int, input_text

MENU = """
1 - список рецептов
2 - поиск рецепта по названию
3 - рецепты, укладывающиеся во время
4 - карточка рецепта с пересчетом порций
5 - добавить рецепт
6 - список пользователей
7 - добавить пользователя
8 - список отзывов
9 - оставить отзыв
10 - удалить отзыв
0 - сохранить и выйти"""


def search_recipes(recipes: List[Recipe]) -> None:
    """Сценарий поиска рецепта по названию."""
    query = input_text("Часть названия: ")
    show_recipes(find_recipe(recipes, query))


def show_quick_recipes(recipes: List[Recipe]) -> None:
    """Сценарий подбора рецептов по времени."""
    limit = input_int("Сколько минут есть на готовку: ", 1)
    show_recipes(sort_recipes(filter_recipes_by_time(recipes, limit)))


def show_card(recipes: List[Recipe], reviews: List[Review]) -> None:
    """Сценарий просмотра карточки рецепта."""
    recipe = find_recipe_by_id(recipes, input_int("ID рецепта: "))
    if recipe is None:
        print("Рецепт не найден")
        return
    servings = input_int("На сколько порций: ", 1, 50)
    show_recipe_card(recipe, servings)
    rating = average_rating(reviews, recipe)
    if rating is None:
        print("Оценок пока нет")
    else:
        print(f"Средняя оценка: {rating}")


def create_new_recipe(recipes: List[Recipe]) -> None:
    """Сценарий добавления рецепта."""
    title = input_text("Название: ")
    category = input_text("Категория: ")
    servings = input_int("Порций: ", 1, 50)
    cook_time = input_int("Время приготовления, мин: ", 1)
    calories = input_int("Калорий на порцию: ", 0)
    recipe = add_recipe(recipes, title, category, servings, cook_time,
                        float(calories))
    print(f"Добавлен рецепт: {recipe}")


def create_new_user(users: List[User]) -> None:
    """Сценарий добавления пользователя."""
    name = input_text("Имя: ")
    email = input_text("Email: ")
    try:
        add_user(users, name, email)
    except ValueError as error:
        print(f"Пользователь не добавлен: {error}")
        return
    print(f"Добавлен пользователь: {users[-1]}")


def create_new_review(
    reviews: List[Review],
    recipes: List[Recipe],
    users: List[User],
) -> None:
    """Сценарий создания отзыва."""
    recipe = find_recipe_by_id(recipes, input_int("ID рецепта: "))
    if recipe is None:
        print("Рецепт не найден")
        return
    user = find_user_by_id(users, input_int("ID пользователя: "))
    if user is None:
        print("Пользователь не найден")
        return
    print(get_review_status(reviews, recipe, user))
    rating = input_int("Оценка 1-5: ", 1, 5)
    comment = input("Комментарий (можно пусто): ").strip()
    review = create_review(reviews, recipe, user, rating, comment)
    if review is None:
        print("Отзыв не создан: уже есть активный отзыв")
    else:
        print(f"Создан отзыв: {review}")


def remove_review(reviews: List[Review]) -> None:
    """Сценарий удаления отзыва."""
    if delete_review(reviews, input_int("ID отзыва: ")):
        print("Отзыв удален")
    else:
        print("Активный отзыв с таким ID не найден")


def main() -> None:
    """Загрузить данные, запустить меню, сохранить данные при выходе."""
    users = load_users()
    recipes = load_recipes()
    reviews = load_reviews(recipes, users)

    while True:
        print(MENU)
        choice = input_int("Выберите пункт: ", 0, 10)
        if choice == 1:
            show_recipes(sort_recipes(recipes))
        elif choice == 2:
            search_recipes(recipes)
        elif choice == 3:
            show_quick_recipes(recipes)
        elif choice == 4:
            show_card(recipes, reviews)
        elif choice == 5:
            create_new_recipe(recipes)
        elif choice == 6:
            show_users(users)
        elif choice == 7:
            create_new_user(users)
        elif choice == 8:
            show_reviews(reviews)
        elif choice == 9:
            create_new_review(reviews, recipes, users)
        elif choice == 10:
            remove_review(reviews)
        else:
            save_users(users)
            save_recipes(recipes)
            save_reviews(reviews)
            print("Данные сохранены")
            break


if __name__ == "__main__":
    main()
