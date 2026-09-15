"""Сервис рецептов. Начальный сценарий: карточка рецепта и пересчет порций."""

import math
from datetime import date

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
servings_wanted_raw = "4"
time_limit_raw = "30"
servings_wanted = int(servings_wanted_raw)
time_limit_min = int(time_limit_raw)

# Пересчет ингредиентов на нужное число порций
scale = servings_wanted / servings_base
spaghetti_needed = math.ceil(spaghetti_g * scale)
bacon_needed = math.ceil(bacon_g * scale)
eggs_needed = math.ceil(eggs_count * scale)
calories_total = round(calories_per_serving * servings_wanted, 1)

# Просмотр карточки рецепта
print("Рецепт: " + recipe_title)
print("Автор: " + author_login)
print("Категория: " + category)
print("Опубликован: " + str(published_at))
print("Время приготовления: " + str(cook_time_min) + " мин")

# Проверка статуса публикации
if is_published:
    print("Статус: опубликован, доступен всем пользователям")
else:
    print("Статус: черновик, виден только автору")

# Пересчет ингредиентов
print("Порций: " + str(servings_wanted) + " (базовый рецепт на "
      + str(servings_base) + ")")
print("Спагетти: " + str(spaghetti_needed) + " г")
print("Бекон: " + str(bacon_needed) + " г")
print("Яйца: " + str(eggs_needed) + " шт")

# Расчет калорийности
print("Калорийность выбранного объема: " + str(calories_total) + " ккал")

if calories_total > 2000:
    print("Внимание: суточная норма калорий превышена")

# Подбор рецепта по ограничению времени
if cook_time_min <= 15:
    speed = "быстрый"
elif cook_time_min <= 40:
    speed = "средний"
else:
    speed = "долгий"

if cook_time_min <= time_limit_min:
    print("Рецепт подходит: " + speed + ", укладывается в "
          + str(time_limit_min) + " мин")
elif cook_time_min <= time_limit_min + 10 and is_published:
    print("Рецепт почти подходит: превышение до 10 мин")
else:
    print("Рецепт не подходит по времени: " + speed)

if not is_published or servings_wanted <= 0:
    print("Рецепт нельзя показать в публичном каталоге")