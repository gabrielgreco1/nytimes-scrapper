import re
import logging
import time
from RPA.Browser.Selenium import Selenium
from utils.url import UrlParser

class NYSearch:
    def __init__(self, driver, query, subject):
        self.logger = logging.getLogger(__name__)
        self.browser = driver
        self.query = query
        self.subject = subject
        self.quantity = 0
        self.url = UrlParser(self.query)

    def open_search(self):
        self.browser.go_to(self.url.construct_url())


    def news_quantity(self):
        element_text = self.browser.get_text("xpath=//*[@id='site-content']/div/div[1]/div[1]/p")
        matches = re.findall(r'\d+', element_text)
        return matches[0]

    def select_subject(self):

        time.sleep(2)
        # Aguarda e clica no botão de cookies
        self.browser.wait_until_element_is_visible("xpath=//*[@id='fides-banner-button-primary']", timeout=20)
        self.browser.click_element("xpath=//*[@id='fides-banner-button-primary']")

        # Aguarda e clica no botão para revelar opções
        self.browser.wait_until_element_is_visible("xpath=//button[@data-testid='search-multiselect-button']", timeout=10)
        self.browser.click_element("xpath=//button[@data-testid='search-multiselect-button']")

        options_labels = self.browser.find_elements("xpath=//ul[@data-testid='multi-select-dropdown-list']/li//span[@class='css-16eo56s']")
        
        for option_label in options_labels:
            option_text = self.browser.get_text(option_label).strip()
            match = re.match(r"([a-zA-Z]+)", option_text)
            if match:
                clean_option_text = match.group(1)
                if clean_option_text.lower() == self.subject.lower():
                    option_input = self.browser.find_element(f"xpath=//span[contains(text(), '{clean_option_text}')]/ancestor::li//input[@type='checkbox']")
                    self.browser.click_element(option_input)
                    break

    def click_show_more(self):
        while True:
            try:
                self.browser.wait_until_element_is_visible("xpath=//button[@data-testid='search-show-more-button']", timeout=10)
                self.browser.click_element("xpath=//button[@data-testid='search-show-more-button']")
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

        # Don't forget to close the browser at the end of your script
        self.browser.close_browser()

# You should initialize the UrlParser and pass it the query parameter according to your specific implementation
# Don't forget to initialize the logging system before using it
