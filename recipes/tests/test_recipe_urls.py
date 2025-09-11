from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_recipes_home_url_is_ok(self):
        url = reverse("recipes:home")
        assert url == "/"

    def test_recipes_category_url_is_ok(self):
        url = reverse("recipes:category", args=(1,))
        assert url == "/recipes/category/1/"

    def test_recipes_recipe_url_is_ok(self):
        url = reverse("recipes:recipe", kwargs={"id": 1})
        assert url == "/recipes/1/"

    def test_recipes_search_url_is_ok(self):
        url = reverse("recipes:search")
        assert url == "/recipes/search/"
