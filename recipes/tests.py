from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_ok(self):
        home_url = reverse("recipes:home")
        assert home_url == "/"
