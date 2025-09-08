from django.core.exceptions import ValidationError
from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_model_recipe_title_raises_error_title_more_65_chars(self):
        max_chars_value = 65
        self.recipe.title = "a" * (max_chars_value + 1)

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
