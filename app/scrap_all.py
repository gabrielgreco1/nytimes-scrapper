from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from infra.logging_config import log_error
class scrap_all:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    # Scrap all the news from the page
    def scrape_list_items(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ol")))
            # Fetch all list items
            list_items = self.driver.find_elements(By.CSS_SELECTOR, "ol > li")
            return list_items
        except TimeoutError as e:
            log_error(f"TimeOut error: {e}")
            return []
        except WebDriverException as e:
            log_error(f"Error while interacting with broswer: {e}")
            return []
        except ConnectionRefusedError as e:
            log_error(f"Error trying connection: {e}")
            return []