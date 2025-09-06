from django.test import TestCase

from recipes.models import Category, User, Recipe


class RecipeTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def make_category(self, name="Category"):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name="John",
        last_name="Potato",
        username="john_potato",
        email="john@potato.com",
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
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
    ):
        if not category_data:
            category_data = {}

        if not author_data:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )
