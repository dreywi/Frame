from django.http import HttpResponse

from homepage.views import page
from models.recipes import find_recipe_by_id
from models.reviews import average_rating
from storage import load_recipes, load_reviews, load_users


def recipes(request):
    items = ""
    for recipe in load_recipes():
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/recipes/{recipe.id}/">{recipe.title}</a>
            <span class="text-muted">
                {recipe.category}, {recipe.cook_time_min} мин
            </span>
        </li>
        """
    content = f"""
    <h1>Рецепты</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Recipe Service - рецепты", content))


def recipe_detail(request, recipe_id):
    recipes_list = load_recipes()
    recipe = find_recipe_by_id(recipes_list, recipe_id)

    if recipe is None:
        content = """
        <h1 class="text-danger">Рецепт не найден</h1>
        <a href="/recipes/" class="btn btn-outline-secondary">
            &larr; к списку рецептов
        </a>
        """
        return HttpResponse(page("Рецепт не найден", content), status=404)

    reviews_list = load_reviews(recipes_list, load_users())
    rating = average_rating(reviews_list, recipe)
    if rating is None:
        rating_html = '<span class="badge bg-secondary">нет оценок</span>'
    else:
        rating_html = f'<span class="badge bg-success">{rating} / 5</span>'

    ingredients = ""
    for ingredient in recipe.ingredients:
        ingredients += f'<li class="list-group-item">{ingredient}</li>'

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{recipe.title}</h5>
            <p class="card-text"><strong>Категория:</strong>
                {recipe.category}</p>
            <p class="card-text"><strong>Порций:</strong>
                {recipe.servings}</p>
            <p class="card-text"><strong>Время:</strong>
                {recipe.cook_time_min} мин ({recipe.speed_label()})</p>
            <p class="card-text"><strong>Калорийность порции:</strong>
                {recipe.calories_per_serving} ккал</p>
            <p class="card-text"><strong>Средняя оценка:</strong>
                {rating_html}</p>
            <h6>Ингредиенты на {recipe.servings} порц.:</h6>
            <ul class="list-group mb-3">{ingredients}</ul>
            <a href="/recipes/" class="btn btn-outline-secondary">
                &larr; к списку рецептов
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(recipe.title, content))
