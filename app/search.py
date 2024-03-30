import re
import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from utils.url import UrlParser  # Supondo que essa parte permaneça inalterada

class NYSearch:
    def __init__(self, driver, query, subject):
        self.logger = logging.getLogger(__name__)
        self.driver = driver
        self.query = query
        self.subject = subject
        self.quantity = 0
        self.url = UrlParser(self.query)

    def open_search(self):
        self.driver.get(self.url.construct_url())

    def news_quantity(self):
        element_text = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='site-content']/div/div[1]/div[1]/p"))
        ).text
        matches = re.findall(r'\d+', element_text)
        return matches[0] if matches else "0"

    def select_subject(self):
        time.sleep(2)
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='fides-banner-button-primary']"))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='search-multiselect-button']"))
        ).click()

        options_labels = self.driver.find_elements(By.XPATH, "//ul[@data-testid='multi-select-dropdown-list']/li//span[@class='css-16eo56s']")
        
        for option_label in options_labels:
            option_text = option_label.text.strip()
            match = re.match(r"([a-zA-Z]+)", option_text)
            if match:
                clean_option_text = match.group(1)
                if clean_option_text.lower() == self.subject.lower():
                    option_input = option_label.find_element(By.XPATH, "./ancestor::li//input[@type='checkbox']")
                    option_input.click()
                    break

    def click_show_more(self):
        while True:
            try:
                show_more_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='search-show-more-button']"))
                )
                show_more_button.click()
            except Exception as e:
                if "timeout" in str(e).lower():
                    break

    def search(self):
        self.logger.info(f"Initiating search with query '{self.query}' and subject '{self.subject}'.")
        self.open_search()
        self.select_subject()
        self.quantity = self.news_quantity()
        self.logger.info(f"Scraping {self.quantity} news")
        self.click_show_more()
        self.driver.quit()
