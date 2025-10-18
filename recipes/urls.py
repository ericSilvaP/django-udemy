from django.urls import path
from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.RecipeListViewHome.as_view(), name="home"),
    path("api/v1/", views.RecipeListViewHomeApi.as_view(), name="home-api"),
    path("recipes/search/", views.RecipeListViewSearch.as_view(), name="search"),
    path("recipes/<int:pk>/", views.RecipeDetail.as_view(), name="recipe"),
    path(
        "recipes/api/v1/<int:pk>/", views.RecipeDetailAPI.as_view(), name="recipe-api"
    ),
    path(
        "recipes/category/<int:category_id>/",
        views.RecipeListViewCategory.as_view(),
        name="category",
    ),
]
