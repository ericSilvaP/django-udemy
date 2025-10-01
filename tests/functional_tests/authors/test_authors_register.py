from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized


class AuthorsRegisterTest(AuthorsBaseTest):
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

        form = self.browser.find_element(
            By.CSS_SELECTOR, ".register-form-container form"
        )

        self.fill_form_dummy_data(form)

        email_field = form.find_element(By.NAME, "email")
        email_field.send_keys("dummy@email.com")
        email_field.send_keys(Keys.ENTER)

        form = self.browser.find_element(
            By.CSS_SELECTOR, ".register-form-container form"
        )

        self.assertIn(error_message, form.text)
