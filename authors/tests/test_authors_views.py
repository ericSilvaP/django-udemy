from django.test import TestCase
from django.urls import resolve, reverse
from authors import views

from authors.tests.login_base import LoginTestBase


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

    def test_authors_login_create_raises_404_with_get(self):
        url = reverse("authors:login_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class AuthorsLoginViewsTest(LoginTestBase):
    def test_authors_recipe_edit_view_is_ok(self):
        self.login()
        url = reverse("authors:dashboard_recipe_edit", kwargs={"id": 1})
        view = resolve(url)
        self.assertIs(view.func, views.dashboard_recipe_edit)

    def test_authors_recipe_edit_view_raises_404_without_valid_recipe(self):
        self.login()
        url = reverse("authors:dashboard_recipe_edit", kwargs={"id": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_logout_redirect_to_login_page_with_logged_user_get_method(self):
        self.login()
        url = reverse("authors:logout")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(url, follow=True)
        self.assertTemplateUsed(response, "authors/pages/login.html")

    def test_logout_redirect_to_login_page_with_logged_user(self):
        self.login()
        url = reverse("authors:logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        response = self.client.post(url, follow=True)
        self.assertTemplateUsed(response, "authors/pages/login.html")
