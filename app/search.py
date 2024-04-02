from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import  TimeoutException, StaleElementReferenceException, NoSuchElementException
from utils.url import UrlParser  
from infra.logging_config import log_info, log_warning, log_error
import re
import time

class NYSearch:
    def __init__(self, driver, query, subject, months):
        self.driver = driver
        self.query = query
        self.subject = subject
        self.months = months
        self.quantity = 0
        self.url = UrlParser(self.query, self.months)

    # Opens the search page
    def open_search(self):
        try:
            self.driver.get(self.url.construct_url())
            log_info(f"Search page opened for URL: {self.url.construct_url()}")
        except Exception as e:
            log_error(f"Failed to open search page: {e}")

    # Retrieves the quantity of news items found
    def news_quantity(self):
        try:
            element = self.driver.find_elements(By.XPATH, """//*[@id="site-content"]/div/div[1]/div[1]/p""")
            element_text = element[0].text
            element_list = element_text.split("\n")
            matches = re.findall(r'\d+', element_list[0])
            return matches[0]
        except TimeoutException:
            log_error("Timeout occurred while trying to find the number of news articles.")
        except NoSuchElementException:
            log_error("The news quantity element was not found on the page.")
        except Exception as e:
            log_error(f"An unexpected error occurred while retrieving news quantity: {e}")
        return "0"

    # Selects the subject from the search filters
    def select_subject(self):
        time.sleep(2)
        try:
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='fides-banner-button-primary']"))
            ).click()

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='search-multiselect-button']"))
            ).click()

            options_labels = self.driver.find_elements(By.XPATH, "//ul[@data-testid='multi-select-dropdown-list']/li//span[@class='css-16eo56s']")
            for option_label in options_labels:
                option_text = option_label.text.strip()
                if option_text.lower() == self.subject.lower():
                    option_input = option_label.find_element(By.XPATH, "./ancestor::li//input[@type='checkbox']")
                    option_input.click()
                    log_info(f"Subject '{self.subject}' selected.")
                    break
                else:
                    log_warning(f"Subject '{self.subject}' not found. Selecting 'Any' by default")
                    break
                    
        except TimeoutException:
            log_warning("Timeout occurred while trying to select the subject.")

    # Clicks the 'Show More' button to load more news items
    def click_show_more(self):
        while True:
            try:
                time.sleep(5)
                show_more_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='search-show-more-button']"))
                )
                show_more_button.click()
            except TimeoutException:
                log_info("All news items loaded.")
                break
            except StaleElementReferenceException:
                continue

    # Performs the search and handles the sequence of actions
    def search(self):
        try:
            log_info(f"Initiating search with query '{self.query}' and subject '{self.subject}' for the past {self.months} months.")
            self.open_search()
            self.select_subject()

            # Get quantity
            self.quantity = self.news_quantity()
            log_info(f"Scrapping {self.quantity} news")

            self.click_show_more()
        except Exception as e:
            log_error(f"An unexpected error occurred during the search: {e}")
        