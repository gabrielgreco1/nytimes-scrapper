from RPA.core.webdriver import start
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class driver:
    def __init__(self):
        self.driver = None

    def set_chrome_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-web-security')
        options.add_argument("--start-maximized")
        options.add_argument('--remote-debugging-port=9222')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return options

    def set_webdriver(self, browser="Chrome"):
        options = self.set_chrome_options()
        # executable_driver_path = cache(browser)
        # if not executable_driver_path:
        #     executable_driver_path = download(browser)
        #     self.logger.warning("Using downloaded driver: %s" % executable_driver_path)
        # else:
        #     self.logger.warning("Using cached driver: %s" % executable_driver_path)

        self.driver = start("Chrome", options=options)
        return self.driver
