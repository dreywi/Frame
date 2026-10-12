from django.http import HttpResponse


def reviews(request):
    return HttpResponse("Список отзывов")


def review_detail(request, review_id):
    return HttpResponse(f"Отзыв {review_id}")
