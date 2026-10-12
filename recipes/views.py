from django.shortcuts import render


from models.recipes import find_recipe_by_id
from models.reviews import average_rating
from storage import load_recipes, load_reviews, load_users


def recipes(request):
    context = {
        "recipes": load_recipes(),
    }
    return render(request, "recipes/recipe_list.html", context)


def recipe_detail(request, recipe_id):
    recipes_list = load_recipes()
    recipe = find_recipe_by_id(recipes_list, recipe_id)
    rating = None
    if recipe is not None:
        reviews_list = load_reviews(recipes_list, load_users())
        rating = average_rating(reviews_list, recipe)
    context = {
        "recipe": recipe,
        "rating": rating,
    }
    return render(
        request,
        "recipes/recipe_detail.html",
        context,
        status=404 if recipe is None else 200,
    )
