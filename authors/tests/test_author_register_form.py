from django.urls import reverse
from django.test import TestCase
from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorsRegisterFormUnitTest(TestCase):
    # ("field", "placeholder_content")
    @parameterized.expand(
        [
            ("first_name", "Ex.: John"),
            ("last_name", "Ex.: Doe"),
            ("username", "Your username"),
            ("email", "Your e-mail"),
            ("password", "Enter your password"),
            ("password_repeat", "Repeat your password"),
        ]
    )
    def test_placeholder_content_is_ok(self, field_name, placeholder_content_test):
        placeholder = RegisterForm().fields[field_name].widget.attrs["placeholder"]
        self.assertEqual(placeholder_content_test, placeholder)

    def test_password_help_text_content_is_ok(self):
        help_text = RegisterForm()["password"].help_text
        self.assertEqual(
            "Password must have at least: one uppercase letter, one lowercase letter and one number. Lenght: minimum 8 characters",
            help_text,
        )

    @parameterized.expand(
        [
            ("first_name", "First Name"),
            ("last_name", "Last Name"),
            ("username", "Username"),
            ("email", "E-mail"),
            ("password", "Password"),
            ("password_repeat", "Repeat Password"),
        ]
    )
    def test_label_is_ok(self, field_name, label_test):
        label = RegisterForm().fields[field_name].label
        self.assertEqual(label, label_test)


class AuthorsRegisterFormIntegrationTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "first_name": "first_name_example",
            "last_name": "last_name_example",
            "username": "user_ex",
            "email": "email@example.com",
            "password": "Exemplo9080",
            "password_repeat": "Exemplo9080",
        }

        return super().setUp()

    @parameterized.expand(
        [
            ("first_name", "Write your first name"),
            ("last_name", "Write your last name"),
            ("username", "Write your username"),
            ("email", "Write your e-mail"),
            ("password", "Password must not be empty"),
            ("password_repeat", "Please, repeat your password"),
        ]
    )
    def test_fields_cannot_be_empty(self, field_name, error_message):
        self.form_data[field_name] = ""
        url = reverse("authors:create")
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(error_message, response.content.decode())
        self.assertIn(error_message, response.context["form"].errors.get(field_name))

    def test_username_field_has_min_length_4(self):
        self.form_data["username"] = "aaa"
        url = reverse("authors:create")
        response = self.client.post(url, follow=True, data=self.form_data)

        self.assertIn(
            "Username must have at least 4 characters", response.content.decode()
        )
        self.assertIn(
            "Username must have at least 4 characters",
            response.context["form"].errors.get("username"),
        )

    def test_username_field_has_max_length_150(self):
        self.form_data["username"] = "a" * 151
        url = reverse("authors:create")
        response = self.client.post(url, follow=True, data=self.form_data)

        self.assertIn(
            "Username must have less than 151 characters", response.content.decode()
        )
        self.assertIn(
            "Username must have less than 151 characters",
            response.context["form"].errors.get("username"),
        )
