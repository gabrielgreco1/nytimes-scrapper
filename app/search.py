import re  
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import  TimeoutException, StaleElementReferenceException
from rpaChallenge.utils.url import UrlParser

class NYSearch:
    def __init__(self, driver, query, subject):
        self.logger = logging.getLogger(__name__)
        self.driver = driver
        self.query = query
        self.subject = subject
        self.quantity = 0
        self.url = UrlParser(self.query)
        self.wait = WebDriverWait(self.driver, 10)

        self.driver.set_window_rect(
                width=1920,
                height=1080)

    def open_search(self):
        self.driver.get(self.url.construct_url())

    def news_quantity(self):
        element = self.driver.find_elements(By.XPATH, """//*[@id="site-content"]/div/div[1]/div[1]/p""")
        element_text = element[0].text
        element_list = element_text.split("\n")
        matches = re.findall(r'\d+', element_list[0])
        return matches[0]

    def select_subject(self):
            
            # cookie button
            time.sleep(2)
            cookies_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="fides-banner-button-primary"]'))
            )
            cookies_button.click()

            # Click on the button to reveal options
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='search-multiselect-button']"))
            )
            button.click()

            # Wait until the dropdown menu is visible
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//ul[@data-testid='multi-select-dropdown-list']"))
            )

            # Get all the options from the dropdown menu
            options_labels = self.driver.find_elements(By.XPATH, "//ul[@data-testid='multi-select-dropdown-list']/li//span[@class='css-16eo56s']")

            # Runs thru each option in the list and click if it matches with the user's input
            for option_label in options_labels:
                option_text = option_label.text.strip()  #  .text to get visible data e .strip() to remove extra spaces
                
                # With regurlar expression we can remove any numerical or special characters that may be present
                match = re.match(r"([a-zA-Z]+)", option_text)
                if match:
                    clean_option_text = match.group(1)  # Get the cleaned option

                # Verify if the text corresponds with the user's input
                if clean_option_text.lower() == self.subject.lower():
                    option_input = option_label.find_element(By.XPATH, "./ancestor::li//input[@type='checkbox']")
                    self.driver.execute_script("arguments[0].click();", option_input) # Forces the selection
                    break
    
    def click_show_more(self):
        while True:
            try:
                # Busca pelo botão "SHOW MORE" a cada iteração para obter a referência mais atual
                show_more_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@data-testid='search-show-more-button']"))
                )
                # Rola até o botão "SHOW MORE"
                self.driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)
                # Espera um pouco para a rolagem acontecer e para o layout da página se ajustar
                time.sleep(1)
                # Clica no botão "SHOW MORE" via JavaScript
                self.driver.execute_script("arguments[0].click();", show_more_button)
            except TimeoutException:
                break
            except StaleElementReferenceException:
                continue

    def search(self):

        self.logger.info(f"Initiating search with query '{self.query}' and subject '{self.subject}'.")
        # Open the search page
        self.open_search()

        # Select the subject
        self.select_subject()

        # Get quantity
        self.quantity = self.news_quantity()
        self.logger.info(f"Scrapping {self.quantity} news")

        # Click in show more button as many as needed
        self.click_show_more()

