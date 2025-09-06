from django.test import TestCase
from django.urls import reverse, resolve

from recipes import views


class RecipeViewsTest(TestCase):
    # home
    def test_recipes_home_view_is_ok(self):
        view = resolve(reverse("recipes:home"))
        assert view.func is views.home

    def test_recipes_home_view_status_code_200_OK(self):
        response = self.client.get(reverse("recipes:home"))
        assert response.status_code == 200

    def test_recipes_home_view_loads_correct_template(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    def test_recipes_home_view_shows_404_message_if_no_recipes_found(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertIn("Não há receitas", response.content.decode())

    # category
    def test_recipes_category_view_is_ok(self):
        view = resolve(reverse("recipes:category", kwargs={"category_id": 1000}))
        assert view.func is views.category

    def test_recipes_category_view_404_without_if_no_recipes_found(self):
        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1000})
        )
        assert response.status_code == 404

    # recipe
    def test_recipes_recipe_view_is_ok(self):
        view = resolve(reverse("recipes:recipe", kwargs={"id": 1000}))
        assert view.func is views.recipe

    def test_recipes_recipe_view_404_without_if_no_recipe_found(self):
        response = self.client.get(reverse("recipes:recipe", kwargs={"id": 1000}))
        assert response.status_code == 404
