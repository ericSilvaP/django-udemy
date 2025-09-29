from pathlib import Path
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = "chromedriver.exe"
CHROMEDRIVER_PATH = ROOT_PATH / "bin" / CHROMEDRIVER_NAME
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"


def make_brave_browser(*options):
    chrome_options = webdriver.ChromeOptions()

    for opt in options:
        chrome_options.add_argument(opt)

    chrome_options.binary_location = BRAVE_PATH
    chrome_service = Service(executable_path=str(CHROMEDRIVER_PATH))
    browser = webdriver.Chrome(options=chrome_options, service=chrome_service)
    return browser


if __name__ == "__main__":
    browser = make_brave_browser()
    browser.get("https://www.google.com.br/")
