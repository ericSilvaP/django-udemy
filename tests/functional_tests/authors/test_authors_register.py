import pytest
from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):
    def get_form(self):
        return self.browser.find_element(
            By.CSS_SELECTOR, ".register-form-container form"
        )

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, "input")

        for field in fields:
            if field.is_displayed():
                field.send_keys(" " * 20)

    @parameterized.expand(
        [
            "Write your first name",
            "Write your last name",
            "Write your username",
            "Password must not be empty",
            "Please, repeat your password",
        ]
    )
    def test_fields_with_spaces_error_messages(self, error_message):
        self.browser.get(self.live_server_url + "/authors/register/")

        form = self.get_form()

        self.fill_form_dummy_data(form)

        email_field = form.find_element(By.NAME, "email")
        email_field.send_keys("dummy@email.com")
        email_field.send_keys(Keys.ENTER)

        form = self.get_form()

        self.assertIn(error_message, form.text)

    def test_invalid_email_error_message(self):
        self.browser.get(self.live_server_url + "/authors/register/")

        form = self.get_form()
        self.fill_form_dummy_data(form)
        email_field = form.find_element(By.NAME, "email")
        email_field.clear()
        email_field.send_keys("dummy@email")
        email_field.send_keys(Keys.ENTER)

        # form reselect after page refresh
        form = self.get_form()

        self.assertIn("Informe um endereço de email válido.", form.text)

    def test_passwords_doesnt_match_error_message(self):
        self.browser.get(self.live_server_url + "/authors/register/")

        form = self.get_form()

        self.fill_form_dummy_data(form)

        password_field = form.find_element(By.NAME, "password")
        password_repeat_field = form.find_element(By.NAME, "password_repeat")

        password_field.send_keys("password1")
        password_repeat_field.send_keys("password2")
        password_repeat_field.send_keys(Keys.ENTER)

        form = self.get_form()
        self.assertIn("Passwords must be equals", form.text)

    def test_register_form_correctly_filled_message(self):
        self.browser.get(self.live_server_url + "/authors/register/")

        form = self.get_form()

        first_name = form.find_element(By.NAME, "first_name")
        last_name = form.find_element(By.NAME, "last_name")
        username = form.find_element(By.NAME, "username")
        email = form.find_element(By.NAME, "email")
        password = form.find_element(By.NAME, "password")
        password_repeat = form.find_element(By.NAME, "password_repeat")

        first_name.send_keys("first")
        last_name.send_keys("last")
        username.send_keys("user")
        email.send_keys("abc@email.com")
        password.send_keys("abcd1234")
        password_repeat.send_keys("abcd1234")
        password_repeat.send_keys(Keys.ENTER)

        self.assertIn(
            "Usuário cadastrado com sucesso",
            self.browser.find_element(By.TAG_NAME, "body").text,
        )
