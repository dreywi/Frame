from django.http import HttpResponse


def recipes(request):
    return HttpResponse("Список рецептов")


def recipe_detail(request, recipe_id):
    return HttpResponse(f"Рецепт {recipe_id}")
