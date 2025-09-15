from django.urls import reverse

from recipes.models import Category, Recipe
from recipes.tests.test_recipe_base import RecipeTestBase
from unittest.mock import patch


class RecipePaginationTest(RecipeTestBase):
    def setUp(self) -> None:
        for i in range(20):
            self.make_recipe(
                slug=f"slug-test-{i}",
                author_data={
                    "first_name": "João",
                    "last_name": "Silva",
                    "username": f"testuser_{i}",
                    "email": f"test_{i}@email.com",
                },
            )
        return super().setUp()

    def test_home_page_has_correct_pagination(self):
        with patch("recipes.views.PER_PAGE", new=9):

            # page 1
            response = self.client.get(reverse("recipes:home"))
            page = response.context["recipes"]

            paginator = page.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 9)
            self.assertEqual(len(paginator.get_page(2)), 9)
            self.assertEqual(len(paginator.get_page(3)), 2)

    def test_category_page_returns_expected_number_of_items(self):
        recipe = self.make_recipe()
        response = self.client.get(
            reverse(
                "recipes:category",
                kwargs={"category_id": getattr(recipe.category, "id")},
            )
        )

        page = response.context["recipes"]

        self.assertEqual(len(page), 1)

    # @patch("recipes.views.PER_PAGE", new=9)
    def test_search_page_has_correct_pagination(self):
        with patch("recipes.views.PER_PAGE", new=9):
            # page 1
            response = self.client.get(reverse("recipes:search") + "?q=e")
            page = response.context["recipes"]

            paginator = page.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 9)
            self.assertEqual(len(paginator.get_page(2)), 9)
            self.assertEqual(len(paginator.get_page(3)), 2)
