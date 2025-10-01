from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from utils.browser import make_brave_browser


class AuthorsBaseTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_brave_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
