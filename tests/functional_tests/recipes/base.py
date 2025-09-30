from recipes.tests.test_recipe_base import RecipeMixin
from utils.browser import make_brave_browser
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class RecipeBaseFunctionalTest(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self) -> None:
        self.browser = make_brave_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
