from django.http import HttpResponse

from homepage.views import page
from models.reviews import find_review_by_id
from storage import load_recipes, load_reviews, load_users


def load_all_reviews():
    return load_reviews(load_recipes(), load_users())


def review_badge(review):
    if review.is_deleted:
        return '<span class="badge bg-secondary">удален</span>'
    return '<span class="badge bg-success">активен</span>'


def reviews(request):
    items = ""
    for review in load_all_reviews():
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/reviews/{review.id}/">
                {review.recipe.title} - {review.rating}/5
            </a>
            {review_badge(review)}
        </li>
        """
    content = f"""
    <h1>Отзывы</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Recipe Service - отзывы", content))


def review_detail(request, review_id):
    review = find_review_by_id(load_all_reviews(), review_id)

    if review is None:
        content = """
        <h1 class="text-danger">Отзыв не найден</h1>
        <a href="/reviews/" class="btn btn-outline-secondary">
            &larr; к списку отзывов
        </a>
        """
        return HttpResponse(page("Отзыв не найден", content), status=404)

    comment = review.comment or "без комментария"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Отзыв №{review.id}</h5>
            <p class="card-text"><strong>Рецепт:</strong>
                <a href="/recipes/{review.recipe.id}/">
                    {review.recipe.title}</a></p>
            <p class="card-text"><strong>Пользователь:</strong>
                {review.user.name}</p>
            <p class="card-text"><strong>Оценка:</strong>
                {review.rating} / 5</p>
            <p class="card-text"><strong>Комментарий:</strong>
                {comment}</p>
            <p class="card-text"><strong>Статус:</strong>
                {review_badge(review)}</p>
            <a href="/reviews/" class="btn btn-outline-secondary">
                &larr; к списку отзывов
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Отзыв №{review.id}", content))
