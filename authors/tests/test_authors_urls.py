from django.test import TestCase
from django.urls import reverse


class AuthorsURLsTest(TestCase):
    def test_authors_register_url_is_ok(self):
        url = reverse("authors:register")
        self.assertEqual(url, "/authors/register/")

    def test_authors_register_create_url_is_ok(self):
        url = reverse("authors:create")
        self.assertEqual(url, "/authors/register/create/")
