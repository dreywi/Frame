from django.http import HttpResponse


def page(title, content):
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/recipes/">Рецепты</a>
        <a class="nav-link" href="/reviews/">Отзывы</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    content = """
    <h1 class="display-4">Recipe Service</h1>
    <p class="lead">Сервис кулинарных рецептов с отзывами и оценками.</p>
    <p>Основные разделы:</p>
    <a href="/recipes/" class="btn btn-primary me-2">Рецепты</a>
    <a href="/reviews/" class="btn btn-secondary">Отзывы</a>
    """
    return HttpResponse(page("Recipe Service", content))
