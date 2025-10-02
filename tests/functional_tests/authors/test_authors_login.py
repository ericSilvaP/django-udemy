import pytest
from .base import AuthorsBaseTest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_created_user_can_login(self):
        username = "user_test"
        password = "password_test"
        User.objects.create_user(username=username, password=password)

        self.browser.get(self.live_server_url + "/authors/login/")

        form = self.browser.find_element(By.CSS_SELECTOR, ".login-form-container form")
        username_field = form.find_element(By.NAME, "username")
        password_field = form.find_element(By.NAME, "password")

        username_field.send_keys(username)
        password_field.send_keys(password)

        form.submit()

        form = self.browser.find_element(By.CSS_SELECTOR, ".login-form-container form")

        self.assertIn(
            f"You are logged in with {username}",
            self.browser.find_element(By.TAG_NAME, "body").text,
        )
