from django.urls import reverse
import pytest

from .login_base import LoginTestBase


@pytest.mark.integration_test
class LoginFormTest(LoginTestBase):
    def get_logout_url(self):
        return reverse("authors:logout")

    def test_created_user_can_login(self):
        url = reverse("authors:login_create")
        response = self.client.post(
            url,
            data={"username": self.username, "password": self.password},
            follow=True,
        )
        self.assertIn("Sucessfully logged.", response.content.decode())

    def test_logout_redirect_to_login_page_without_logged_user(self):
        url = self.get_logout_url()
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        response = self.client.post(url, follow=True)
        self.assertTemplateUsed(response, "authors/pages/login.html")

    def test_invalid_form_error_message(self):
        url = reverse("authors:login_create")
        error_message = "Error to validate form data."
        response = self.client.post(
            url, data={"username": " ", "password": " "}, follow=True
        )
        self.assertIn(error_message, response.content.decode())

    def test_incorrect_username_or_password_error_message(self):
        url = reverse("authors:login_create")
        response = self.client.post(
            url,
            data={"username": "username_test", "password": "password_test"},
            follow=True,
        )
        self.assertIn("Incorrect password or username.", response.content.decode())
