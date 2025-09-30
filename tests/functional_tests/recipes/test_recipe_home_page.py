import time
from unittest.mock import patch
from selenium.webdriver.common.by import By

from recipes.tests.test_recipe_base import RecipeMixin
from .base import RecipeBaseFunctionalTest
import pytest


@pytest.mark.functional_test
class RecipesHomePageTest(RecipeBaseFunctionalTest):
    @patch("recipes.views.PER_PAGE", new=3)
    def test_the_test(self):
        self.make_recipes_in_batch(5)
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Não há receitas", body)
