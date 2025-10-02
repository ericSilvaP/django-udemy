from django.test import TestCase
from django.urls import reverse
import pytest
from django.contrib.auth.models import User


@pytest.mark.unit_test
class LoginFormTestUnitTest(TestCase):
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


class LoginFormTestIntegrated(TestCase):
    def test_created_user_can_login(self):
        username = "user_test"
        password = "password_test"
        User.objects.create_user(username=username, password=password)

        url = reverse("authors:login_create")
        response = self.client.post(
            url, data={"username": username, "password": password}, follow=True
        )
        self.assertIn("Sucessfully logged.", response.content.decode())
