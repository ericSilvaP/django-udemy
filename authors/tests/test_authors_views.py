from django.test import TestCase
from django.urls import resolve, reverse
from authors import views


class AuthorsViewsTest(TestCase):
    def test_authors_register_view_is_ok(self):
        view = resolve(reverse("authors:register"))
        self.assertIs(view.func, views.register_view)

    def test_authors_register_create_view_is_ok(self):
        view = resolve(reverse("authors:register_create"))
        self.assertIs(view.func, views.register_create)

    def test_authors_login_view_is_ok(self):
        view = resolve(reverse("authors:login"))
        self.assertIs(view.func, views.login_view)

    def test_authors_login_create_view_is_ok(self):
        view = resolve(reverse("authors:login_create"))
        self.assertIs(view.func, views.login_create)

    def test_authors_login_create_raises_error_with_get(self):
        url = reverse("authors:login_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
