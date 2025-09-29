from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from utils.browser import make_brave_browser


class RecipesHomePageTest(StaticLiveServerTestCase):
    def test_the_test(self):
        browser = make_brave_browser("--headless")
        browser.get(self.live_server_url)
        body = browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Não há receitas", body)
