from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import  TimeoutException, WebDriverException

class scrap_all:
    def __init__(self, driver)  -> list:
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    # Scrap all the news from the page
    def scrape_list_items(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ol")))
            print('List all items.............')
            # Fetch all list items
            list_items = self.driver.find_elements(By.CSS_SELECTOR, "ol > li")
            return list_items
        except TimeoutError:
            return []
        except WebDriverException as e:
            print(f"Erro ao interagir com o WebDriver: {e}")
            return []
        except ConnectionRefusedError as e:
            print(f"Erro de conexão: {e}")
            return []