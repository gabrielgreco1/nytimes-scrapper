from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def driverSettings():
    # Define as opções do Chrome para execução em modo headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    # Inicializa o navegador com as opções especificadas
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    return driver
