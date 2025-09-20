from django.test import TestCase
from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorsRegisterFormTestUnitTest(TestCase):

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
