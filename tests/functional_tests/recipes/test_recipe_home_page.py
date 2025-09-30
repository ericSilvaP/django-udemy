from selenium.webdriver.common.by import By
from .base import RecipeBaseFunctionalTest
import pytest


@pytest.mark.functional_test
class RecipesHomePageTest(RecipeBaseFunctionalTest):
    def test_the_test(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Não há receitas", body)
