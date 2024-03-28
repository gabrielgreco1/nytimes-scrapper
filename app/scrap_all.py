from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class scrap_all:
    def __init__(self, driver)  -> list:
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    # Scrap all the news from the page
    def scrape_list_items(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ol")))
            # Fetch all list items
            list_items = self.driver.find_elements(By.CSS_SELECTOR, "ol > li")
            return list_items
        except TimeoutError:
            return []