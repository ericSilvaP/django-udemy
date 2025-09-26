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
