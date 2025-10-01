import time
from unittest.mock import patch
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from dotenv import load_dotenv

from .base import RecipeBaseFunctionalTest
import pytest

load_dotenv()


@pytest.mark.functional_test
class RecipesHomePageTest(RecipeBaseFunctionalTest):
    def test_recipes_home_error_message_without_recipes(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Não há receitas", body)

    def test_search_input_can_find_correct_recipe(self):
        recipes = self.make_recipes_in_batch(5)

        needed_title = "Recipe Title Test"
        recipes[0].title = needed_title
        recipes[0].save()

        # user open the browser
        self.browser.get(self.live_server_url)

        # click in search bar
        search_input = self.browser.find_element(
            By.CSS_SELECTOR,
            ".search-input",
        )

        # search for recipe
        search_input.send_keys(needed_title)
        search_input.send_keys(Keys.ENTER)

        # search recult must appear correctly
        body = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn(needed_title, body)
