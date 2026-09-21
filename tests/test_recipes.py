import pytest

from models import Ingredient, Recipe
from models.recipes import (
    add_recipe,
    filter_recipes_by_time,
    find_recipe,
    sort_recipes,
)


@pytest.fixture
def carbonara():
    return Recipe(1, "Паста карбонара", "Основные блюда", 2, 25, 640.5,
                  [Ingredient("Спагетти", 200, "г"),
                   Ingredient("Яйца", 2, "шт")])


def test_recipe_creation(carbonara):
    assert carbonara.id == 1
    assert carbonara.title == "Паста карбонара"
    assert carbonara.servings == 2
    assert len(carbonara.ingredients) == 2


def test_recipe_str(carbonara):
    assert str(carbonara) == (
        "[1] Паста карбонара (Основные блюда), 25 мин, 2 порц."
    )


def test_fits_time(carbonara):
    assert carbonara.fits_time(30)
    assert carbonara.fits_time(25)
    assert not carbonara.fits_time(20)


def test_speed_label(carbonara):
    assert carbonara.speed_label() == "средний"


def test_total_calories(carbonara):
    assert carbonara.total_calories(4) == 2562.0


def test_scaled_ingredients(carbonara):
    scaled = carbonara.scaled_ingredients(4)
    assert [item.amount for item in scaled] == [400, 4]
    assert carbonara.ingredients[0].amount == 200


def test_scaled_ingredients_invalid_servings(carbonara):
    with pytest.raises(ValueError):
        carbonara.scaled_ingredients(0)


def test_validate_servings():
    assert Recipe.validate_servings(1)
    assert not Recipe.validate_servings(0)
    assert not Recipe.validate_servings(51)


def test_recipe_invalid_servings():
    with pytest.raises(ValueError):
        Recipe(1, "Омлет", "Завтраки", 0, 10, 320.0)


def test_ingredient_invalid_amount():
    with pytest.raises(ValueError):
        Ingredient("Соль", 0, "г")


def test_add_recipe(carbonara):
    recipes = [carbonara]
    recipe = add_recipe(recipes, "Омлет", "Завтраки", 1, 10, 320.0)
    assert recipe.id == 2
    assert recipes[-1] is recipe


def test_find_recipe(carbonara):
    assert find_recipe([carbonara], "КАРБО") == [carbonara]
    assert find_recipe([carbonara], "борщ") == []


def test_filter_and_sort():
    slow = Recipe(1, "Борщ", "Супы", 6, 120, 210.0)
    fast = Recipe(2, "Омлет", "Завтраки", 1, 10, 320.0)
    medium = Recipe(3, "Паста", "Основные блюда", 2, 25, 640.5)
    recipes = [slow, fast, medium]
    assert filter_recipes_by_time(recipes, 30) == [fast, medium]
    assert sort_recipes(recipes) == [fast, medium, slow]
