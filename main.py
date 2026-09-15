
import math
from datetime import date


def get_publication_status(is_published):
    "Проверка статуса публикации рецепта."
    if is_published:
        return "опубликован, доступен всем пользователям"
    return "черновик, виден только автору"


def scale_amount(amount, servings_base, servings_wanted):
    "Пересчет количества одного ингредиента на нужное число порций."
    return math.ceil(amount * servings_wanted / servings_base)


def get_total_calories(calories_per_serving, servings_wanted):
    "Расчет калорийности выбранного объема порций."
    return round(calories_per_serving * servings_wanted, 1)


def get_speed_label(cook_time_min):
    "Категория рецепта по времени приготовления."
    if cook_time_min <= 15:
        return "быстрый"
    elif cook_time_min <= 40:
        return "средний"
    return "долгий"


def get_time_match(cook_time_min, time_limit_min, is_published):
    "Подбор рецепта по ограничению времени приготовления."
    if cook_time_min <= time_limit_min:
        return "подходит: укладывается в " + str(time_limit_min) + " мин"
    elif cook_time_min <= time_limit_min + 10 and is_published:
        return "почти подходит: превышение до 10 мин"
    return "не подходит по времени"


def print_recipe_card(title, author, category, published_at, cook_time_min):
    "Вывод карточки рецепта."
    print("Рецепт: " + title)
    print("Автор: " + author)
    print("Категория: " + category)
    print("Опубликован: " + str(published_at))
    print("Время приготовления: " + str(cook_time_min) + " мин")


# Данные рецепта
recipe_title = "Паста карбонара"
author_login = "chef_ivanov"
category = "Основные блюда"
servings_base = 2
cook_time_min = 25
calories_per_serving = 640.5
spaghetti_g = 200.0
bacon_g = 150.0
eggs_count = 2
is_published = True
published_at = date(2026, 9, 15)

# Запрос пользователя
servings_wanted = int("4")
time_limit_min = int("30")

print_recipe_card(recipe_title, author_login, category, published_at,
                  cook_time_min)
print("Статус: " + get_publication_status(is_published))

# Пересчет ингредиентов
print("Порций: " + str(servings_wanted) + " (базовый рецепт на "
      + str(servings_base) + ")")
print("Спагетти: "
      + str(scale_amount(spaghetti_g, servings_base, servings_wanted)) + " г")
print("Бекон: "
      + str(scale_amount(bacon_g, servings_base, servings_wanted)) + " г")
print("Яйца: "
      + str(scale_amount(eggs_count, servings_base, servings_wanted)) + " шт")

# Калорийность
calories_total = get_total_calories(calories_per_serving, servings_wanted)
print("Калорийность выбранного объема: " + str(calories_total) + " ккал")
if calories_total > 2000:
    print("Внимание: суточная норма калорий превышена")

# Подбор по времени
print("Рецепт " + get_time_match(cook_time_min, time_limit_min, is_published)
      + " (" + get_speed_label(cook_time_min) + ")")

if not is_published or servings_wanted <= 0:
    print("Рецепт нельзя показать в публичном каталоге")