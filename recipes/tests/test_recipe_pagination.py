from django.urls import reverse

from recipes.models import Recipe
from recipes.tests.test_recipe_base import RecipeTestBase


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
        # page 1
        response = self.client.get(reverse("recipes:home"))
        page = response.context["recipes"]

        self.assertEqual(len(page), 9)

        # page 2
        response = self.client.get(reverse("recipes:home") + "?page=2")
        page = response.context["recipes"]

        self.assertEqual(len(page), 9)

        # page 3
        response = self.client.get(reverse("recipes:home") + "?page=3")
        page = response.context["recipes"]

        self.assertEqual(len(page), 2)

    def test_category_page_has_correct_pagination(self):
        # page 1
        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1})
        )
        page = response.context["recipes"]

        self.assertEqual(len(page), 1)

    def test_search_page_has_correct_pagination(self):
        # page 1
        response = self.client.get(reverse("recipes:search") + "?q=e")
        page = response.context["recipes"]

        self.assertEqual(len(page), 9)

        # page 2
        response = self.client.get(reverse("recipes:search") + "?page=2&q=e")
        page = response.context["recipes"]

        self.assertEqual(len(page), 9)

        # page 3
        response = self.client.get(reverse("recipes:search") + "?page=3&q=e")
        page = response.context["recipes"]

        self.assertEqual(len(page), 2)
