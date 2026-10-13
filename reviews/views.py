from django.shortcuts import render


from models.reviews import find_review_by_id
from storage import load_recipes, load_reviews, load_users


def load_all_reviews():
    return load_reviews(load_recipes(), load_users())


def reviews(request):
    context = {
        "reviews": load_all_reviews(),
    }
    return render(request, "reviews/review_list.html", context)


def review_detail(request, review_id):
    review = find_review_by_id(load_all_reviews(), review_id)
    context = {
        "review": review,
    }
    return render(
        request,
        "reviews/review_detail.html",
        context,
        status=404 if review is None else 200,
    )
