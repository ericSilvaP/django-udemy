from django.urls import path
from . import views

app_name = "authors"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("register/create/", views.register_create, name="register_create"),
    path("login/", views.login_view, name="login"),
    path("login/create/", views.login_create, name="login_create"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.Dashboard.as_view(), name="dashboard"),
    path(
        "dashboard/recipe/<int:id>/edit/",
        views.DashboardRecipe.as_view(),
        name="dashboard_recipe_edit",
    ),
    path(
        "dashboard/recipe/create/",
        views.DashboardRecipe.as_view(),
        name="dashboard_create_recipe",
    ),
    path(
        "dashboard/recipe/delete/<int:id>",
        views.DashboardDeleteRecipe.as_view(),
        name="dashboard_delete_recipe",
    ),
]
