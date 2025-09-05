from django.test import TestCase
from django.urls import reverse, resolve

from recipes import views


class RecipeViewsTest(TestCase):
    def test_recipes_home_view_is_ok(self):
        view = resolve(reverse("recipes:home"))
        assert view.func is views.home

    def test_recipes_category_view_is_ok(self):
        view = resolve(reverse("recipes:category", kwargs={"category_id": 1}))
        assert view.func is views.category

    def test_recipes_recipe_view_is_ok(self):
        view = resolve(reverse("recipes:recipe", kwargs={"id": 1}))
        assert view.func is views.recipe
