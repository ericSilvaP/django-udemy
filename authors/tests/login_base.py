from django.test import TestCase
from django.contrib.auth.models import User


class LoginTestBase(TestCase):
    def setUp(self) -> None:
        self.username = "user_test"
        self.password = "password_test"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )
        return super().setUp()

    def login(self):
        return self.client.login(username=self.username, password=self.password)
