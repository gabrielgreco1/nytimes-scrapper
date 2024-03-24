from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import config
import urllib.parse
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
import pandas as pd
import os
import json
import time

class NYTSearch:
    def __init__(self, driver, query, months):
        self.driver = driver
        self.query = query
        self.months = months
        self.wait = WebDriverWait(self.driver, 10)
        self.filepath = f"{config.path}\\{query}"
        self.filepath = self.filepath.replace(" ","_")
        self.excelpath = f"{self.filepath}\\news.xlsx"
        self.images_path = f"{self.filepath}\\images\\"
        
        

    def create_directory(self, filepath):
        directory = os.path.dirname(filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def calculate_dates(self):
        endDate = datetime.now()
        startDate = endDate - relativedelta(months=max(self.months, 1))
        if self.months == 0:
            startDate = endDate - relativedelta(months=1)
        return endDate.strftime("%Y-%m-%d"), startDate.strftime("%Y-%m-%d")

    def encode_query(self):
        return urllib.parse.quote(self.query)

    def construct_url(self, formatted_endDate, formatted_startDate):
        query_encoded = self.encode_query()
        return f"https://www.nytimes.com/search?dropmab=false&endDate={formatted_endDate}&query={query_encoded}&sort=newest&startDate={formatted_startDate}"

    def open_search(self):
        formatted_endDate, formatted_startDate = self.calculate_dates()
        url = self.construct_url(formatted_endDate, formatted_startDate)
        print('Opening the site')
        self.driver.get(url)

    def click_show_more(self):
        print('Finding all news..')
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
                # Se o botão "SHOW MORE" não for encontrado após o tempo de espera, sai do loop
                print("Botão 'SHOW MORE' não encontrado. Saindo do loop.")
                break
            except StaleElementReferenceException:
                # Se o botão se tornar obsoleto durante a busca, tenta novamente na próxima iteração
                print("Referência obsoleta do elemento. Tentando encontrar novamente...")
                continue
                
    def scrape_list_items(self):
        print("Reading all news...")
        try:
            # Wait until the list appears on the webpage
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ol")))
            # Fetch all list items
            list_items = self.driver.find_elements(By.CSS_SELECTOR, "ol > li")
            return list_items
        except TimeoutError:
            print("The list did not load in time")
            return []

    def scrape_item_details(self, list_item):
        # Assuming list_item is a WebElement object
        newsData = {}

        # Extract headings
        newsData["headings"] = [heading.text for heading in list_item.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6")]

        # Extract <span> element
        newsData["date"] = [span.text for span in list_item.find_elements(By.CSS_SELECTOR, "span")]

        # Extract <p> elements
        newsData["paragraphs"] = [p.text for p in list_item.find_elements(By.CSS_SELECTOR, "p")]

        # Extract <a> elements
        newsData["links"] = [a.get_attribute("href") for a in list_item.find_elements(By.CSS_SELECTOR, "a")]

        # Extract <img> inside <figure>
        figures = list_item.find_elements(By.CSS_SELECTOR, "div > figure")
        imagesUrls = [fig.find_element(By.TAG_NAME, "img").get_attribute("src") for fig in figures if fig.find_element(By.TAG_NAME, "img")]
        return {
            "newsData": newsData,
            "imageUrls": imagesUrls
        }
    
    def download_image(self, url, path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(path, "wb") as file:
                file.write(response.content)

    def save_to_xlsx(self, data):
        print('Saving to xlsx...')
        # Define o texto base do link indesejado para a verificação
        undesired_links_texts = [
                                "https://www.nytimes.com/search?dropmab=false",
                                "https://www.nytimes.com/topic/"
        ]        
        # Verifica se algum link na lista contém o texto base
        if any(any(base_text in link for base_text in undesired_links_texts) for link in data["newsData"]["links"]):
            print("Encontrado link com texto base indesejado, registro ignorado.")
            return
        
         # separar função
        
        # Desempacota os dados
        news_data = data["newsData"]
        image_urls = data["imageUrls"]
        
        # Seleciona o segundo parágrafo de "paragraphs", conforme especificado
        selected_paragraph = news_data["paragraphs"][1] if len(news_data["paragraphs"]) > 1 else None
        
        # Preparando os dados para DataFrame
        data_for_df = {
            "headings": [news_data["headings"][0]] if news_data["headings"] else [None],
            "date": [news_data["date"][0]] if news_data["date"] else [None],
            "paragraphs": [selected_paragraph],
            "links": [news_data["links"][0]] if news_data["links"] else [None],
            "image_urls": [image_urls[0]] if image_urls else "No image available",
            "imageFilepath":news_data["savePath"]
        }
        
        df = pd.DataFrame(data_for_df)
        
        # Se o arquivo já existe, carrega o DataFrame existente e anexa os novos dados
        if os.path.exists(self.excelpath):
            with pd.ExcelWriter(self.excelpath, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
                # Lê o arquivo Excel existente e o DataFrame da planilha específica
                try:
                    existing_data_df = pd.read_excel(self.excelpath, sheet_name="News Data")
                    # Anexa os novos dados
                    updated_df = pd.concat([existing_data_df, df], ignore_index=True)
                    # Salva o DataFrame atualizado no arquivo, substituindo a planilha existente
                    updated_df.to_excel(writer, sheet_name="News Data", index=False)
                except ValueError:
                    # Se a planilha não existir, apenas escreve os novos dados
                    df.to_excel(writer, sheet_name="News Data", index=False)
        else:
            # Se o arquivo não existe, cria um novo e salva os dados
            with pd.ExcelWriter(self.excelpath, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="News Data", index=False)

    def run(self):
        print('Starting the automation')
        # Open the search page
        self.open_search()

        # Click in show more button as many as needed
        self.click_show_more()

        # Scrape all list items
        list_items = self.scrape_list_items()

        # Creating the main directorys
        self.create_directory(self.filepath)
        time.sleep(0.5)
        self.create_directory(self.images_path)

        for item in list_items:
            # Scrape details for each item
            data = self.scrape_item_details(item)
            if data:
                print("-------------------------------------------------------------")

                for url in data["imageUrls"]:
                    filename = f"{data["newsData"]["headings"]}.jpg".replace("[", "").replace("]", "").replace("?", "")
                    save_path = f"{self.images_path}{filename}"
                    self.download_image(url, save_path)
                data['newsData']['savePath'] = save_path
                self.save_to_xlsx(data)
               
        print('Automation finished')       
        self.driver.quit()
        return []