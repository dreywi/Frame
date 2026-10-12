from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("recipes/", include("recipes.urls")),
    path("reviews/", include("reviews.urls")),
]

handler404 = "homepage.views.page_not_found"
