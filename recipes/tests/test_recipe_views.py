from django.test import TestCase
from django.urls import reverse, resolve
from recipes.models import Recipe, Category, User

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

    def test_recipes_home_template_loads_recipes(self):
        category = Category.objects.create(name="Category")
        author = User.objects.create_user(
            first_name="John",
            last_name="Potato",
            username="john_potato",
            email="john@potato.com",
        )
        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title="Recipe title",
            description="Recipe Description",
            slug="recipe-slug",
            preparation_time=10,
            preparation_time_unit="Minutos",
            servings=5,
            servings_unit="Porções",
            preparation_steps="Forma de Preparo da Receita",
            preparation_steps_is_html=False,
            is_published=True,
        )

        response = self.client.get(reverse("recipes:home"))
        content = response.content.decode()
        recipes_context = response.context["recipes"]

        self.assertIn(recipe.title, content)
        self.assertEqual(len(recipes_context), 1)

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
