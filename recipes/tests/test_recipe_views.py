from urllib import response
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

    def test_recipes_home_view_status_code_200_OK(self):
        response = self.client.get(reverse("recipes:home"))
        assert response.status_code == 200

    def test_recipes_home_view_loads_correct_template(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    def test_recipes_home_view_shows_not_found_message_without_recipes_in_db(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertIn("Não há receitas", response.content.decode())
