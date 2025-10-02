from django.test import TestCase
from django.urls import reverse


class AuthorsURLsTest(TestCase):
    def test_authors_register_url_is_ok(self):
        url = reverse("authors:register")
        self.assertEqual(url, "/authors/register/")

    def test_authors_register_create_url_is_ok(self):
        url = reverse("authors:register_create")
        self.assertEqual(url, "/authors/register/create/")

    def test_authors_login_view_url_is_ok(self):
        url = reverse("authors:login")
        self.assertEqual(url, "/authors/login/")

    def test_authors_login_create_url_is_ok(self):
        url = reverse("authors:login_create")
        self.assertEqual(url, "/authors/login/create/")

    def test_authors_logout_url_is_ok(self):
        url = reverse("authors:logout")
        self.assertEqual(url, "/authors/logout/")
