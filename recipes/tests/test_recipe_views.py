from urllib import response
from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
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

    def test_recipes_home_template_loads_recipes(self):
        self.make_recipe()

        response = self.client.get(reverse("recipes:home"))
        content = response.content.decode()

        self.assertIn("Recipe title", content)

    def test_recipes_home_template_dont_load_unpublished_recipe(self):
        self.make_recipe(is_published=False)

        response = self.client.get(reverse("recipes:home"))
        content = response.content.decode()

        self.assertIn("Não há receitas", content)

    # category
    def test_recipes_category_view_is_ok(self):
        view = resolve(
            reverse(
                "recipes:category",
                kwargs={"category_id": 1000},
            )
        )
        assert view.func is views.category

    def test_recipes_category_view_404_without_if_no_recipes_found(self):
        response = self.client.get(
            reverse(
                "recipes:category",
                kwargs={"category_id": 1000},
            )
        )
        assert response.status_code == 404

    def test_recipes_category_template_loads_recipes(self):
        needed_title = "This is a category page"

        self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse(
                "recipes:category",
                kwargs={"category_id": 1},
            )
        )
        content = response.content.decode()

        self.assertIn(needed_title, content)

    def test_recipes_category_template_dont_load_unpublished_recipe(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                "recipes:category",
                kwargs={"category_id": getattr(recipe.category, "id")},
            )
        )

        self.assertEqual(response.status_code, 404)

    # recipe
    def test_recipes_recipe_view_is_ok(self):
        view = resolve(reverse("recipes:recipe", kwargs={"id": 1000}))
        assert view.func is views.recipe

    def test_recipes_recipe_view_404_without_if_no_recipe_found(self):
        response = self.client.get(
            reverse(
                "recipes:recipe",
                kwargs={"id": 1000},
            )
        )
        assert response.status_code == 404

    def test_recipes_recipe_template_loads_recipes(self):
        needed_title = "This is a recipe detail page - It load one recipe"

        self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse(
                "recipes:recipe",
                kwargs={"id": 1},
            )
        )
        content = response.content.decode()

        self.assertIn(needed_title, content)

    def test_recipes_recipe_template_dont_load_unpublished_recipe(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                "recipes:recipe",
                kwargs={"id": getattr(recipe, "id")},
            )
        )

        self.assertEqual(response.status_code, 404)

    # search
    def test_recipes_search_view_is_ok(self):
        view = resolve(reverse("recipes:search"))
        self.assertIs(view.func, views.search)

    def test_recipes_search_template_loads_recipes(self):
        response = self.client.get(reverse("recipes:search"))
        self.assertTemplateUsed(response, "recipes/pages/search.html")

    def test_recipes_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse("recipes:search"))
        self.assertEqual(response.status_code, 404)

    def test_recipes_search_raises_404_if_only_spaces_in_search_term(self):
        response = self.client.get(f"{reverse("recipes:search")}?q=+")
        self.assertEqual(response.status_code, 404)
