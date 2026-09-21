"""Рецепты и ингредиенты."""

from typing import List, Optional


class Ingredient:
    """Ингредиент рецепта с количеством."""

    def __init__(self, name: str, amount: float, unit: str) -> None:
        if amount <= 0:
            raise ValueError(f"Количество должно быть больше 0: {name}")
        self.name = name
        self.amount = amount
        self.unit = unit

    def scaled(self, factor: float) -> "Ingredient":
        """Вернуть ингредиент с количеством, умноженным на factor."""
        return Ingredient(self.name, round(self.amount * factor, 1),
                          self.unit)

    def __str__(self) -> str:
        return f"{self.name}: {self.amount:g} {self.unit}"


class Recipe:
    """Кулинарный рецепт."""

    def __init__(
        self,
        recipe_id: int,
        title: str,
        category: str,
        servings: int,
        cook_time_min: int,
        calories_per_serving: float,
        ingredients: Optional[List[Ingredient]] = None,
    ) -> None:
        if not Recipe.validate_servings(servings):
            raise ValueError(f"Некорректное число порций: {servings}")
        self.id = recipe_id
        self.title = title
        self.category = category
        self.servings = servings
        self.cook_time_min = cook_time_min
        self.calories_per_serving = calories_per_serving
        self.ingredients: List[Ingredient] = (
            ingredients if ingredients is not None else []
        )

    @staticmethod
    def validate_servings(servings: int) -> bool:
        """Проверить, что число порций в допустимых пределах."""
        return 0 < servings <= 50

    def fits_time(self, time_limit_min: int) -> bool:
        """Проверить, укладывается ли рецепт в ограничение по времени."""
        return self.cook_time_min <= time_limit_min

    def speed_label(self) -> str:
        """Категория рецепта по времени приготовления."""
        if self.cook_time_min <= 15:
            return "быстрый"
        if self.cook_time_min <= 40:
            return "средний"
        return "долгий"

    def total_calories(self, servings: int) -> float:
        """Калорийность заданного числа порций."""
        return round(self.calories_per_serving * servings, 1)

    def scaled_ingredients(self, servings: int) -> List[Ingredient]:
        """Пересчитать ингредиенты на заданное число порций."""
        if not Recipe.validate_servings(servings):
            raise ValueError(f"Некорректное число порций: {servings}")
        factor = servings / self.servings
        return [ingredient.scaled(factor) for ingredient in self.ingredients]

    def __str__(self) -> str:
        return (f"[{self.id}] {self.title} ({self.category}), "
                f"{self.cook_time_min} мин, {self.servings} порц.")


def add_recipe(
    recipes: List[Recipe],
    title: str,
    category: str,
    servings: int,
    cook_time_min: int,
    calories_per_serving: float,
) -> Recipe:
    """Создать рецепт, добавить в коллекцию и вернуть его."""
    new_id = max((recipe.id for recipe in recipes), default=0) + 1
    recipe = Recipe(new_id, title, category, servings, cook_time_min,
                    calories_per_serving)
    recipes.append(recipe)
    return recipe


def find_recipe(recipes: List[Recipe], query: str) -> List[Recipe]:
    """Найти рецепты по названию."""
    query = query.lower()
    return [recipe for recipe in recipes if query in recipe.title.lower()]


def find_recipe_by_id(recipes: List[Recipe],
                      recipe_id: int) -> Optional[Recipe]:
    """Найти рецепт по идентификатору."""
    for recipe in recipes:
        if recipe.id == recipe_id:
            return recipe
    return None


def filter_recipes_by_time(recipes: List[Recipe],
                           time_limit_min: int) -> List[Recipe]:
    """Отобрать рецепты, укладывающиеся в ограничение по времени."""
    return [recipe for recipe in recipes if recipe.fits_time(time_limit_min)]


def sort_recipes(recipes: List[Recipe]) -> List[Recipe]:
    """Отсортировать рецепты по времени приготовления."""
    return sorted(recipes, key=lambda recipe: recipe.cook_time_min)


def show_recipes(recipes: List[Recipe]) -> None:
    """Вывести список рецептов."""
    if not recipes:
        print("Рецептов нет")
        return
    for recipe in recipes:
        print(recipe)


def show_recipe_card(recipe: Recipe, servings: int) -> None:
    """Вывести карточку рецепта, пересчитанную на число порций."""
    print(recipe)
    print(f"Скорость: {recipe.speed_label()}")
    print(f"Ингредиенты на {servings} порц.:")
    for ingredient in recipe.scaled_ingredients(servings):
        print(f"  {ingredient}")
    print(f"Калорийность: {recipe.total_calories(servings)} ккал")
