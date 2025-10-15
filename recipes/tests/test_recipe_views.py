from unittest.mock import patch
from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    # home
    def test_recipes_home_view_is_ok(self):
        view = resolve(reverse("recipes:home"))
        assert view.func.view_class is views.RecipeListViewHome

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
        assert view.func.view_class is views.RecipeListViewCategory

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

    def test_recipes_category_template_does_not_loads_unpublished_recipe(self):
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
        view = resolve(reverse("recipes:recipe", kwargs={"pk": 1000}))
        assert view.func.view_class is views.RecipeDetail

    def test_recipes_recipe_view_404_without_if_no_recipe_found(self):
        response = self.client.get(
            reverse(
                "recipes:recipe",
                kwargs={"pk": 1000},
            )
        )
        assert response.status_code == 404

    def test_recipes_recipe_template_loads_recipes(self):
        needed_title = "This is a recipe detail page - It load one recipe"

        self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse(
                "recipes:recipe",
                kwargs={"pk": 1},
            )
        )
        content = response.content.decode()

        self.assertIn(needed_title, content)

    def test_recipes_recipe_template_does_not_loads_unpublished_recipe(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                "recipes:recipe",
                kwargs={"pk": getattr(recipe, "id")},
            )
        )

        self.assertEqual(response.status_code, 404)

    # search
    def test_recipes_search_view_is_ok(self):
        view = resolve(reverse("recipes:search"))
        self.assertIs(view.func.view_class, views.RecipeListViewSearch)

    def test_recipes_search_template_loads_recipes(self):
        response = self.client.get(reverse("recipes:search") + "?q=test")
        self.assertTemplateUsed(response, "recipes/pages/search.html")

    def test_recipes_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse("recipes:search"))
        self.assertEqual(response.status_code, 404)

    def test_recipes_search_raises_404_if_only_spaces_in_search_term(self):
        response = self.client.get(f"{reverse("recipes:search")}?q=+")
        self.assertEqual(response.status_code, 404)

    def test_recipes_search_search_term_is_on_title_and_escaped(self):
        response = self.client.get(f"{reverse("recipes:search")}?q=<test>")
        self.assertIn(
            "Pesquisa por &quot;&lt;test&gt;&quot; |",
            response.content.decode(),
        )

    def test_recipes_search_search_correct_recipes_by_title(self):
        # testar pesquisa por duas receitas individualmente, testar se titulo renderiza no template, testar pesquisa por ambas

        title1 = "This is title for Recipe 01"
        title2 = "This is title for Recipe 02"

        recipe1 = self.make_recipe(
            title=title1, slug="recipe-test-01", author_data={"username": "one"}
        )
        recipe2 = self.make_recipe(
            title=title2, slug="recipe-test-02", author_data={"username": "two"}
        )

        url_search_path = reverse("recipes:search")
        response1 = self.client.get(f"{url_search_path}?q={title1}")
        response2 = self.client.get(f"{url_search_path}?q={title2}")
        response_both = self.client.get(f"{url_search_path}?q=this")

        self.assertIn(recipe1, response1.context["recipes"])
        self.assertNotIn(recipe2, response1.context["recipes"])
        self.assertIn(title1, response1.content.decode())
        self.assertNotIn(title2, response1.content.decode())

        self.assertIn(recipe2, response2.context["recipes"])
        self.assertNotIn(recipe1, response2.context["recipes"])
        self.assertIn(title2, response2.content.decode())
        self.assertNotIn(title1, response2.content.decode())

        self.assertIn(recipe1, response_both.context["recipes"])
        self.assertIn(recipe2, response_both.context["recipes"])
        self.assertIn(title1, response_both.content.decode())
        self.assertIn(title2, response_both.content.decode())

    def test_recipes_search_search_correct_recipes_by_description(self):
        # testar pesquisa por duas receitas individualmente, testar se descrição renderiza no template, testar pesquisa por ambas

        description_1 = "This is preparation steps for Recipe 01"
        desciption_2 = "This is preparation steps for Recipe 02"

        recipe1 = self.make_recipe(
            description=description_1,
            slug="recipe-test-01",
            author_data={"username": "one"},
        )
        recipe2 = self.make_recipe(
            description=desciption_2,
            slug="recipe-test-02",
            author_data={"username": "two"},
        )

        url_search_path = reverse("recipes:search")
        response1 = self.client.get(f"{url_search_path}?q={description_1}")
        response2 = self.client.get(f"{url_search_path}?q={desciption_2}")
        response_both = self.client.get(f"{url_search_path}?q=this")

        self.assertIn(recipe1, response1.context["recipes"])
        self.assertNotIn(recipe2, response1.context["recipes"])
        self.assertIn(description_1, response1.content.decode())
        self.assertNotIn(desciption_2, response1.content.decode())

        self.assertIn(recipe2, response2.context["recipes"])
        self.assertNotIn(recipe1, response2.context["recipes"])
        self.assertIn(desciption_2, response2.content.decode())
        self.assertNotIn(description_1, response2.content.decode())

        self.assertIn(recipe1, response_both.context["recipes"])
        self.assertIn(recipe2, response_both.context["recipes"])
        self.assertIn(description_1, response_both.content.decode())
        self.assertIn(desciption_2, response_both.content.decode())

    def test_invalid_page_query_uses_page_one(self):
        for i in range(8):
            kwargs = {"slug": f"r{i}", "author_data": {"username": f"u{i}"}}
            self.make_recipe(**kwargs)

        with patch("recipes.views.PER_PAGE", new=3):
            response = self.client.get(reverse("recipes:home") + "?page=12A")
            self.assertEqual(response.context["recipes"].number, 1)
            response = self.client.get(reverse("recipes:home") + "?page=2")
            self.assertEqual(response.context["recipes"].number, 2)
            response = self.client.get(reverse("recipes:home") + "?page=3")
            self.assertEqual(response.context["recipes"].number, 3)
